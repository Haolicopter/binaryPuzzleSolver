#!/usr/bin/env python3

import helpers


class Matrix:

    def __init__(self, browser, size, cellCssClass='puzzlecel'):
        self.browser = browser
        self.size = size
        self.cellCssClass = cellCssClass
        self.totalCount = 0
        self.count = {
            'row': [], 'col': []
        }
        for i in range(size):
            self.count['row'].append(
                {
                    'total': 0,
                    0: 0,
                    1: 0
                }
            )
            self.count['col'].append(
                {
                    'total': 0,
                    0: 0,
                    1: 0
                }
            )
        self.completeRows = []
        self.completeCols = []
        self.nearCompleteRows = []
        self.nearCompleteCols = []

        self.load()
        self.countRowsAndCols()
        self.updateCompleteness()

    # Load matrix from game with given URL
    def load(self):
        cells = self.browser.find_elements_by_class_name(self.cellCssClass)
        self.values = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                stringValue = cells[i*self.size+j].text
                intValue = int(stringValue) if stringValue.strip() else None
                if intValue is not None:
                    self.totalCount += 1
                row.append(intValue)
            self.values.append(row)

    # Print the current matrix
    def print(self):
        print('Printing matrix...')
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.values[i][j])
            print(row)
            print('Row total count: ' + str(self.count['row'][i]['total']))
            print('Row zeros count: ' + str(self.count['row'][i][0]))
            print('Row ones count: ' + str(self.count['row'][i][1]))
            print('Col total count: ' + str(self.count['col'][i]['total']))
            print('Col zeros count: ' + str(self.count['col'][i][0]))
            print('Col ones count: ' + str(self.count['col'][i][1]))
        print('Complete rows:')
        print(self.completeRows)
        print('Complete cols:')
        print(self.completeCols)

    # Draw the matrix on browser
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

    # Add one cell to the matrix
    def addOne(self, i, j, value):
        if value is None:
            return
        self.totalCount += 1
        self.count['row'][i][value] += 1
        self.count['row'][i]['total'] += 1
        self.count['col'][j][value] += 1
        self.count['col'][j]['total'] += 1
        self.updateCurrentRowAndColCompleteness(i, j)

    # Check if the matrix is complete
    def isComplete(self):
        return self.totalCount == self.size * self.size

    # Check if index is in range
    def indexIsInRange(self, row, col):
        if row < 0 or row > self.size-1:
            return False
        if col < 0 or col > self.size-1:
            return False
        return True

    # Set the adjacent cells of neighbours to the other number
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
                        self.addOne(adjRow, adjCol, 1 - current)

    # Count the not none cells in rows/columns
    def countRowsAndCols(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.values[i][j] is not None:
                    self.addOne(i, j, self.values[i][j])

    # Check for complete and near complete rows/columns
    def updateCompleteness(self):
        for i in range(self.size):
            self.updateCurrentRowAndColCompleteness(i, i)

    # Check for complete and near complete for current row/column
    def updateCurrentRowAndColCompleteness(self, i, j):
        # We can handle up to this many missing cells
        threshold = 3
        # This row is completed
        if self.count['row'][i]['total'] == self.size:
            self.completeRows.append(i)
        # This row is near complete
        elif self.count['row'][i]['total'] + threshold >= self.size:
            self.nearCompleteRows.append(i)

        # This col is completed
        if self.count['col'][j]['total'] == self.size:
            self.completeCols.append(j)
        # This col is near complete
        elif self.count['col'][j]['total'] + threshold >= self.size:
            self.nearCompleteCols.append(j)
