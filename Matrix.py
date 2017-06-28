#!/usr/bin/env python3

import helpers


class Matrix:

    def __init__(self, browser, size, cellCssClass='puzzlecel'):
        self.browser = browser
        self.size = size
        self.cellCssClass = cellCssClass
        self.count = 0

    def readMatrix(self):
        cells = self.browser.find_elements_by_class_name(self.cellCssClass)
        matrix = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                stringValue = cells[i*self.size+j].text
                intValue = int(stringValue) if stringValue.strip() else None
                if intValue is not None:
                    self.count += 1
                row.append(intValue)
            matrix.append(row)
        return matrix

    def printMatrix(self, matrix):
        print('Printing matrix...')
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(matrix[i][j])
            print(row)

    def writeMatrix(self, newMatrix):
        for i in range(self.size):
            for j in range(self.size):
                value = newMatrix[i][j]
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
