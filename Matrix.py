#!/usr/bin/env python3

import helpers


class Matrix:

    def __init__(self, browser, size, cellCssClass='puzzlecel'):
        self.browser = browser
        self.size = size
        self.cellCssClass = cellCssClass
        self.count = 0
        self.load()

    def load(self):
        cells = self.browser.find_elements_by_class_name(self.cellCssClass)
        self.values = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                stringValue = cells[i*self.size+j].text
                intValue = int(stringValue) if stringValue.strip() else None
                if intValue is not None:
                    self.count += 1
                row.append(intValue)
            self.values.append(row)

    def print(self):
        print('Printing matrix...')
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.values[i][j])
            print(row)

    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.values[i][j]
                cellCssId = '#cel_' + str(i+1) + '_' + str(j+1)
                cell = self.browser.find_element_by_css_selector(cellCssId)
                if value == 1:
                    helpers.setCellToOne(self.browser, cell)
                elif value == 0:
                    helpers.setCellToZero(self.browser, cell)

    def addOne(self):
        self.count += 1

    def isCompleted(self):
        return self.count == self.size * self.size

    def indexIsInRange(self, row, col):
        if row < 0 or row > self.size-1:
            return False
        if col < 0 or col > self.size-1:
            return False
        return True

    def setNeighbours(self, neighbours, current):
        for neighbour in neighbours:
            row = neighbour['row']
            col = neighbour['col']
            # If neighbour exists and equal to the current cell
            if (self.indexIsInRange(row, col) and
                    self.values[row][col] == current):
                for adjacentCell in neighbour['adjacentCells']:
                    adjRow = adjacentCell['row']
                    adjCol = adjacentCell['col']
                    if (self.indexIsInRange(adjRow, adjCol) and
                            self.values[adjRow][adjCol] is None):
                        # Set the adjcent to the other number
                        self.values[adjRow][adjCol] = 1 - current
                        self.addOne()
