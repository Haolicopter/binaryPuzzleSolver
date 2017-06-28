#!/usr/bin/env python3

import helpers
import time
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

    def setLevel(self, difficulty, level, size=12):
        self.difficulty = difficulty
        self.level = level
        self.size = size

    def getUrl(self):
        return 'http://binarypuzzle.com/puzzles.php?' \
            + 'size=' + str(self.size) \
            + '&level=' + str(self.difficulty) \
            + '&nr=' + str(self.level)

    def printLevel(self):
        print('Difficulty = ' + str(self.difficulty))
        print('Level = ' + str(self.level))
        print('Size = ' + str(self.size))

    def play(self):
        self.browser.get(self.getUrl())
        # Count down to the show, get ready
        # time.sleep(2)

        self.matrix = Matrix(self.browser, self.size)
        self.cells = self.matrix.readMatrix()
        self.matrix.printMatrix(self.cells)

        maxTries = 100
        for t in range(maxTries):
            if self.matrix.isCompleted():
                break
            for i in range(self.size):
                for j in range(self.size):
                    self.findPairs(i, j)
                    self.avoidTrios(i, j)
            self.completeRowsAndCols()

        # Eliminate impossible combinations based on completed rows/columns:
        # No identical rows/columns are allowed.

        # Eliminate other impossible combinations.

        # Guess and try.

        self.matrix.printMatrix(self.cells)
        if self.matrix.isCompleted():
            print('Yay! We did it!')
        else:
            print('Still need more work')
        self.matrix.writeMatrix(self.cells)

    # Find pairs:
    # Because no more than two similar numbers next to or below each other
    # are allowed, pairs can be supplementen with the other number.
    def findPairs(self, i, j):
        current = self.cells[i][j]
        if current is None:
            return

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
        self.setNeighbours(neighbours, current)

    def indexInRange(self, row, col):
        if row < 0 or row > self.size-1:
            return False
        if col < 0 or col > self.size-1:
            return False
        return True

    def setNeighbours(self, neighbours, current):
        for neighbour in neighbours:
            # If neighbour exists and equal to the current cell
            if self.indexInRange(neighbour['row'], neighbour['col']) and self.cells[neighbour['row']][neighbour['col']] == current:
                for adjacentCell in neighbour['adjacentCells']:
                    if self.indexInRange(adjacentCell['row'], adjacentCell['col']) and self.cells[adjacentCell['row']][adjacentCell['col']] is None:
                        self.cells[adjacentCell['row']][adjacentCell['col']] = 1 - current
                        self.matrix.addOne()
                        # TODO: how to update adjacent cells pairs without hitting recurrsion limit?
                        # self.findPairs(adjacentCell['row'], adjacentCell['col'])

    # Avoid trios:
    # If two cells contain the same number with an empty cell in between,
    # this empty cell should contain the other number.
    def avoidTrios(self, i, j):
        current = self.cells[i][j]
        if current is None:
            return

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
        self.setNeighbours(neighbours, current)

    # Complete rows and columns:
    # Each row and each column should contain an equal number of 1s and 0s.
    def completeRowsAndCols(self):
        # For each row
        for i in range(self.size):
            zeroCount = 0
            oneCount = 0
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    zeroCount += 1
                elif self.cells[i][j] == 1:
                    oneCount += 1
            if zeroCount == self.size/2 and oneCount < self.size/2:
                for j in range(self.size):
                    if self.cells[i][j] is None:
                        self.cells[i][j] = 1
                        self.matrix.addOne()
            elif oneCount == self.size/2 and zeroCount < self.size/2:
                for j in range(self.size):
                    if self.cells[i][j] is None:
                        self.cells[i][j] = 0
                        self.matrix.addOne()
        # For each col
        for j in range(self.size):
            zeroCount = 0
            oneCount = 0
            for i in range(self.size):
                if self.cells[i][j] == 0:
                    zeroCount += 1
                elif self.cells[i][j] == 1:
                    oneCount += 1
            if zeroCount == self.size/2 and oneCount < self.size/2:
                for i in range(self.size):
                    if self.cells[i][j] is None:
                        self.cells[i][j] = 1
                        self.matrix.addOne()
            elif oneCount == self.size/2 and zeroCount < self.size/2:
                for i in range(self.size):
                    if self.cells[i][j] is None:
                        self.cells[i][j] = 0
                        self.matrix.addOne()
