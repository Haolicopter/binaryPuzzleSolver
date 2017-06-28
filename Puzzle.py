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

        matrix = Matrix(self.browser, self.size)
        self.cells = matrix.readMatrix()
        matrix.printMatrix(self.cells)

        for i in range(self.size):
            for j in range(self.size):
                self.findPairs(i, j)

        # Avoid trios:
        # If two cells contain the same number with an empty cell in between,
        # this empty cell should contain the other number.

        # Complete rows and columns:
        # Each row and each column should contain an equal number of 1s and 0s.

        # Eliminate impossible combinations based on completed rows/columns:
        # No identical rows/columns are allowed.

        # Eliminate other impossible combinations.

        # Guess and try.
        matrix.printMatrix(self.cells)
        matrix.writeMatrix(self.cells)

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
        for neighbour in neighbours:
            # If neighbour exists and equal to the current cell
            if self.indexInRange(neighbour['row'], neighbour['col']) and self.cells[neighbour['row']][neighbour['col']] == current:
                for adjacentCell in neighbour['adjacentCells']:
                    if self.indexInRange(adjacentCell['row'], adjacentCell['col']):
                        self.cells[adjacentCell['row']][adjacentCell['col']] = 1 - current
                        # TODO: how to update adjacent cells pairs without hitting recurrsion limit?
                        # self.findPairs(adjacentCell['row'], adjacentCell['col'])

    def indexInRange(self, row, col):
        if row < 0 or row > self.size-1:
            return False
        if col < 0 or col > self.size-1:
            return False
        return True
