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

        # Keep trying
        maxTries = 100
        for t in range(maxTries):
            if self.matrix.isCompleted():
                break
            for i in range(self.size):
                for j in range(self.size):
                    # Only check for cell with values
                    if self.matrix.values[i][j] is None:
                        continue
                    self.findPairs(i, j)
                    self.avoidTrios(i, j)
            self.completeRowsAndCols()

        # Eliminate impossible combinations based on completed rows/columns:
        # No identical rows/columns are allowed.

        # Eliminate other impossible combinations.

        # Guess and try.

        if self.matrix.isCompleted():
            print('Yay! We did it!')
        else:
            print('Still need more work')
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
            zeroCount = 0
            oneCount = 0
            for j in range(self.size):
                if self.matrix.values[i][j] == 0:
                    zeroCount += 1
                elif self.matrix.values[i][j] == 1:
                    oneCount += 1
            if zeroCount == self.size/2 and oneCount < self.size/2:
                for j in range(self.size):
                    if self.matrix.values[i][j] is None:
                        self.matrix.values[i][j] = 1
                        self.matrix.addOne()
            elif oneCount == self.size/2 and zeroCount < self.size/2:
                for j in range(self.size):
                    if self.matrix.values[i][j] is None:
                        self.matrix.values[i][j] = 0
                        self.matrix.addOne()
        # For each col
        for j in range(self.size):
            zeroCount = 0
            oneCount = 0
            for i in range(self.size):
                if self.matrix.values[i][j] == 0:
                    zeroCount += 1
                elif self.matrix.values[i][j] == 1:
                    oneCount += 1
            if zeroCount == self.size/2 and oneCount < self.size/2:
                for i in range(self.size):
                    if self.matrix.values[i][j] is None:
                        self.matrix.values[i][j] = 1
                        self.matrix.addOne()
            elif oneCount == self.size/2 and zeroCount < self.size/2:
                for i in range(self.size):
                    if self.matrix.values[i][j] is None:
                        self.matrix.values[i][j] = 0
                        self.matrix.addOne()
