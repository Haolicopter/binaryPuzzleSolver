#!/usr/bin/env python3

import helpers
import os
from Matrix import Matrix


class Puzzle:
    # Puzzle constants
    SIZE = {
        '6*6': 6,
        '8*8': 8,
        '10*10': 10,
        '12*12': 12,
        '14*14': 14
    }
    DIFFICULTY = {
        'easy': 1,
        'medium': 2,
        'hard': 3,
        'very hard': 4
    }
    LEVEL = range(101)  # from 1 to 100

    def __init__(self):
        # Get Selenium Chrome Driver
        self.browser = helpers.getChromeDriver()

    def set(self, difficulty, level, size=12):
        self.difficulty = difficulty
        self.level = level
        self.size = size
        self.showConfig()
        # Load game into browser
        self.browser.get(self.getUrl())
        # Load matrix from game
        self.matrix = Matrix(self.browser, self.size)

    # Construct binary puzzle URL
    def getUrl(self):
        return 'http://binarypuzzle.com/puzzles.php?' \
            + 'size=' + str(self.size) \
            + '&level=' + str(self.difficulty) \
            + '&nr=' + str(self.level)

    # Show puzzle configuration
    def showConfig(self):
        print('Difficulty = ' + str(self.difficulty))
        print('Level = ' + str(self.level))
        print('Size = ' + str(self.size))

    # Let's play!
    def play(self):
        # This is the matrix we start with
        self.matrix.print()

        # Keep trying until exhausted
        maxTries = 200
        for t in range(maxTries):
            if self.matrix.isComplete():
                break
            for i in range(self.size):
                for j in range(self.size):
                    # Only check for cell with values
                    if self.matrix.values[i][j] is None:
                        continue
                    self.findPairs(i, j)
                    self.avoidTrios(i, j)
            self.completeRowsAndCols()
            self.solveNearComplete()

        if self.matrix.isComplete():
            if self.matrix.isCorrect():
                print('Yay! We did it!')
            else:
                print('Crap the solution is incorrect!')
        else:
            print(
                'Need more work.. We solved '
                + str(self.matrix.totalCount)
                + ' out of '
                + str(self.size*self.size))

        # This is the matrix we end up with
        self.matrix.print()

    # Find pairs:
    # Because no more than two similar numbers next to or below each other
    # are allowed, pairs can be supplementen with the other number.
    def findPairs(self, i, j):
        neighbours = [
            {
                'row': i-1, 'col': j,
                'adjacentCells': [
                    {'row': i-2, 'col': j},
                    {'row': i+1, 'col': j}
                ]
            },
            {
                'row': i+1, 'col': j,
                'adjacentCells': [
                    {'row': i-1, 'col': j},
                    {'row': i+2, 'col': j}
                ]
            },
            {
                'row': i, 'col': j-1,
                'adjacentCells': [
                    {'row': i, 'col': j-2},
                    {'row': i, 'col': j+1}
                ]
            },
            {
                'row': i, 'col': j+1,
                'adjacentCells': [
                    {'row': i, 'col': j-1},
                    {'row': i, 'col': j+2}
                ]
            }
        ]
        self.matrix.setNeighbours(neighbours, i, j)

    # Avoid trios:
    # If two cells contain the same number with an empty cell in between,
    # this empty cell should contain the other number.
    def avoidTrios(self, i, j):
        neighbours = [
            {
                'row': i-2, 'col': j,
                'adjacentCells': [
                    {'row': i-1, 'col': j}
                ]
            },
            {
                'row': i+2, 'col': j,
                'adjacentCells': [
                    {'row': i+1, 'col': j}
                ]
            },
            {
                'row': i, 'col': j-2,
                'adjacentCells': [
                    {'row': i, 'col': j-1}
                ]
            },
            {
                'row': i, 'col': j+2,
                'adjacentCells': [
                    {'row': i, 'col': j+1}
                ]
            }
        ]
        self.matrix.setNeighbours(neighbours, i, j)

    # Complete rows and columns:
    # Each row and each column should contain an equal number of 1s and 0s.
    def completeRowsAndCols(self):
        for v in self.matrix.vectorTypes:
            for i in range(self.size):
                # Current vector is only missing 1s
                if (self.matrix.count[v][i][0] == self.size/2 and
                        self.matrix.count[v][i][1] < self.size/2):
                    val = 1
                # Current vector is only missing 0s
                elif (self.matrix.count[v][i][1] == self.size/2 and
                        self.matrix.count[v][i][0] < self.size/2):
                    val = 0
                # Current vector is missing a mix of 1s and 0s
                else:
                    continue

                # Set the missing cells to the value we know
                print(v + ' ' + str(i) + ' already has all the ' + str(1-val) +
                      's. Setting all missing cells (listed below) at ' +
                      v + ' ' + str(i) + ' to ' + str(val))
                for j in range(self.size):
                    (row, col) = self.matrix.getRowAndColIndexes(v, i, j)
                    if self.matrix.values[row][col] is None:
                        print('Setting cell (' + str(row) + ', ' + str(col) +
                              ') to ' + str(val))
                        self.matrix.setCell(row, col, val)

    # Try solving near complete rows/cols
    def solveNearComplete(self):
        if len(self.matrix.nearCompleteVectors) == 0:
            return
        for (vectorType, i, missingCount) in self.matrix.nearCompleteVectors:
            self.eliminateImpossibleCombinations(vectorType, i, missingCount)

    # Eliminate impossible combinations based on completed rows/columns:
    # No identical rows/columns are allowed.
    def eliminateImpossibleCombinations(self, vectorType, i, missingCount):
        # Lay out all the possible combinations
        candidates = self.matrix.getCandidates(vectorType, i, missingCount)

        wrongCandidates = []
        for candidate in candidates:
            # Check if it violates pairs or trios rules
            if self.matrix.violatesRules(vectorType, candidate):
                wrongCandidates.append(candidate)
                continue
            # Check if it is identical to any rows/columns that are completed
            if self.matrix.hasDuplicatedVectors(vectorType, candidate):
                wrongCandidates.append(candidate)
                continue

        if len(candidates) == len(wrongCandidates):
            return

        for wrongCandidate in wrongCandidates:
            candidates.remove(wrongCandidate)

        candidatesCount = len(candidates)
        hasMessage = False
        message = 'Using eliminateImpossibleCombinations method at ' + \
            vectorType + ' ' + str(i) + ' with ' + str(missingCount) + \
            ' missing cells, we nailed down to ' + str(candidatesCount) + \
            ' possible combo(s)' + os.linesep

        for candidate in candidates:
            line = ''
            for x in range(len(candidate)):
                line += str(candidate[x]['val']) + ', '
            message += line[:-2] + os.linesep

        if candidatesCount == 1:
            message += 'Since this is the only possible combination. ' + \
                'We solved entire ' + vectorType + ' ' + str(i) + os.linesep
            for cell in candidates[0]:
                if cell['isGuess']:
                    hasMessage = True
                    message += 'Setting cell (' + str(cell['row']) + ', ' + \
                        str(cell['col']) + ') to ' + str(cell['val']) + \
                        os.linesep
                    self.matrix.setCell(cell['row'], cell['col'], cell['val'])
        elif candidatesCount > 1:
            message += 'Finding missing cells that all combos agree on' + \
                os.linesep
            for x in range(len(candidates[0])):
                cell = candidates[0][x]
                if cell['isGuess'] is False:
                    continue
                isCommon = True
                for i in range(1, candidatesCount):
                    if cell['val'] != candidates[i][x]['val']:
                        isCommon = False
                        break
                if isCommon:
                    hasMessage = True
                    message += 'Setting cell (' + str(cell['row']) + ', ' + \
                        str(cell['col']) + ') to ' + str(cell['val']) + \
                        os.linesep
                    self.matrix.setCell(cell['row'], cell['col'], cell['val'])

        if hasMessage:
            print(message.rstrip())
