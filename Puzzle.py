#!/usr/bin/env python3

import helpers
from Matrix import Matrix


class Puzzle:
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

    def getUrl(self):
        return 'http://binarypuzzle.com/puzzles.php?' \
            + 'size=' + str(self.size) \
            + '&level=' + str(self.difficulty) \
            + '&nr=' + str(self.level)

    def showConfig(self):
        print('Difficulty = ' + str(self.difficulty))
        print('Level = ' + str(self.level))
        print('Size = ' + str(self.size))

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
                print('Sorry but the solution is not correct')
        else:
            print(
                'Still need more work.. We solved '
                + str(self.matrix.totalCount)
                + ' out of '
                + str(self.size*self.size))
        # Draw the solution matrix on browser
        self.matrix.print()
        self.matrix.draw()

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
        self.matrix.setNeighbours(neighbours, self.matrix.values[i][j])

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
        self.matrix.setNeighbours(neighbours, self.matrix.values[i][j])

    # Complete rows and columns:
    # Each row and each column should contain an equal number of 1s and 0s.
    def completeRowsAndCols(self):
        # For each row
        for i in range(self.size):
            if (self.matrix.count['row'][i][0] == self.size/2 and
                    self.matrix.count['row'][i][1] < self.size/2):
                for j in range(self.size):
                    if self.matrix.values[i][j] is None:
                        self.matrix.setCell(i, j, 1)
            elif (self.matrix.count['row'][i][1] == self.size/2 and
                    self.matrix.count['row'][i][0] < self.size/2):
                for j in range(self.size):
                    if self.matrix.values[i][j] is None:
                        self.matrix.setCell(i, j, 0)
        # For each col
        for j in range(self.size):
            if (self.matrix.count['col'][j][0] == self.size/2 and
                    self.matrix.count['col'][j][1] < self.size/2):
                for i in range(self.size):
                    if self.matrix.values[i][j] is None:
                        self.matrix.setCell(i, j, 1)
            elif (self.matrix.count['col'][j][1] == self.size/2 and
                    self.matrix.count['col'][j][0] < self.size/2):
                for i in range(self.size):
                    if self.matrix.values[i][j] is None:
                        self.matrix.setCell(i, j, 0)

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
        for candidate in candidates:
            print(candidate)
            # Check if it violates pairs or trios rules
            if self.matrix.isIllegal(candidate):
                print('Sorry but is illegal')
                candidates.remove(candidate)
                continue
            # Check if it is identical to any rows/columns that are completed
            if self.matrix.hasDuplicatedVectors(vectorType, candidate):
                print('Sorry but hasDuplicatedVectors')
                candidates.remove(candidate)
                continue

        # If we have one possible combination, this is the answer
        if len(candidates) == 1:
            print('One possible combination!')
            for cell in candidates[0]:
                if cell['isGuess']:
                    self.matrix.setCell(cell['row'], cell['col'], cell['val'])
        # If we have multiple possible combinations, find the common cells
        elif len(candidates) > 1:
            print('Attention! checking ' + str(len(candidates)) + ' candidates...')
            for x in range(len(candidates[0])):
                cell = candidates[0][x]
                if cell['isGuess'] is False:
                    continue
                print('checking cell ' + str(x) + ' with rest of the candidates:')
                isCommon = True
                for i in range(1, len(candidates)):
                    print(str(cell['val']) + ' ?= ' + str(candidates[i][x]['val']))
                    if cell['val'] != candidates[i][x]['val']:
                        isCommon = False
                        break
                if isCommon:
                    self.matrix.setCell(cell['row'], cell['col'], cell['val'])
