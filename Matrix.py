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

        self.vectorTypes = ('row', 'col')
        self.completeVectors = []
        self.nearCompleteVectors = []

        # We can guess up to this many missing cells
        self.maxComboSize = 4

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
        #     print('Row total count: ' + str(self.count['row'][i]['total']))
        #     print('Row zeros count: ' + str(self.count['row'][i][0]))
        #     print('Row ones count: ' + str(self.count['row'][i][1]))
        #     print('Col total count: ' + str(self.count['col'][i]['total']))
        #     print('Col zeros count: ' + str(self.count['col'][i][0]))
        #     print('Col ones count: ' + str(self.count['col'][i][1]))
        # print('Complete vectors:')
        # print(self.completeVectors)
        # print('Near complete vectors:')
        # print(self.nearCompleteVectors)

    # Draw the matrix on browser
    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.values[i][j]
                cellCssId = '#cel_' + str(i+1) + '_' + str(j+1)
                cell = self.browser.find_element_by_css_selector(cellCssId)
                if value == 1:
                    helpers.drawOne(self.browser, cell)
                elif value == 0:
                    helpers.drawZero(self.browser, cell)

    # Set cell at given position to given value
    def addCount(self, i, j, value):
        # Ignore none value
        if value is None:
            return

        self.totalCount += 1
        self.count['row'][i][value] += 1
        self.count['row'][i]['total'] += 1
        self.count['col'][j][value] += 1
        self.count['col'][j]['total'] += 1
        self.updateCurrentVectorCompleteness(i, j)

    # Set cell value and add count
    def setCell(self, i, j, value):
        if value is None:
            return
        if self.values[i][j] is not None:
            return
        # print('Setting ['+str(i)+','+str(j)+'] from ' + str(self.values[i][j]) + ' to '+str(value))
        self.values[i][j] = value
        self.addCount(i, j, value)

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
                        self.setCell(adjRow, adjCol, 1 - current)

    # Count the not none cells in rows/columns
    def countRowsAndCols(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.values[i][j] is not None:
                    self.addCount(i, j, self.values[i][j])

    # Check for complete and near complete rows/columns
    def updateCompleteness(self):
        for i in range(self.size):
            self.updateCurrentVectorCompleteness(i, i)

    # Check for complete and near complete for current row/column
    def updateCurrentVectorCompleteness(self, i, j):
        for vectorType in self.vectorTypes:
            vectorMissingCells = self.size - self.count[vectorType][i]['total']
            vector = (vectorType, i, vectorMissingCells)
            # This vector is complete
            if vectorMissingCells == 0:
                # Add to complete vector list if does not exist
                if vector not in self.completeVectors:
                    self.completeVectors.append(vector)
                # Remove from near complete vector list if exists
                self.nearCompleteVectors = list(filter(
                    lambda v: not (v[0] == vectorType and v[1] == i),
                    self.nearCompleteVectors))
            # This vector is near complete
            elif vectorMissingCells <= self.maxComboSize:
                oldVector = None
                for (vv, ii, mm) in self.nearCompleteVectors:
                    if vv == vectorType and ii == i:
                        oldVector = (vv, ii, mm)
                if oldVector is not None:
                    self.nearCompleteVectors.remove(oldVector)
                self.nearCompleteVectors.append(vector)
                # Sort by number of missing cells
                self.nearCompleteVectors.sort(key=lambda row: row[2])

    # Get all combination given missing number of zeros and ones
    def getCombos(self, vectorType, i, missingCount):
        if missingCount == 2:
            # One zero and one one, no doubt
            return [
                (0, 1),
                (1, 0)
            ]
        elif missingCount == 3:
            if self.count[vectorType][i][0] == self.size/2 - 1:
                # One zero and two ones
                return [
                    (1, 1, 0),
                    (1, 0, 1),
                    (0, 1, 1)
                ]
            elif self.count[vectorType][i][1] == self.size/2 - 1:
                # One one and two zeros
                return [
                    (0, 0, 1),
                    (0, 1, 0),
                    (1, 0, 0)
                ]
        elif missingCount == 4:
            if self.count[vectorType][i][0] == self.size/2 - 1:
                # One zero and three ones
                return [
                    (1, 1, 1, 0),
                    (1, 1, 0, 1),
                    (1, 0, 1, 1),
                    (0, 1, 1, 1)
                ]
            elif self.count[vectorType][i][0] == self.size/2 - 2:
                # Two zeros and two ones
                return [
                    (0, 0, 1, 1),
                    (0, 1, 0, 1),
                    (0, 1, 1, 0),
                    (1, 1, 0, 0),
                    (1, 0, 1, 0),
                    (1, 0, 0, 1)
                ]
            elif self.count[vectorType][i][1] == self.size/2 - 1:
                # One one and three zeros
                return [
                    (0, 0, 0, 1),
                    (0, 0, 1, 0),
                    (0, 1, 0, 0),
                    (1, 0, 0, 0)
                ]

        return []

    # Get row/col candidates
    def getCandidates(self, vectorType, i, missingCount):
        candidates = []
        combos = self.getCombos(vectorType, i, missingCount)
        for combo in combos:
            count = 0
            candidate = []
            for j in range(self.size):
                (row, col) = self.getRowAndColIndexes(vectorType, i, j)
                # Load from combo
                if self.values[row][col] is None:
                    val = combo[count]
                    count += 1
                    isGuess = True
                # Load from current cell
                else:
                    val = self.values[row][col]
                    isGuess = False

                candidate.append({
                    'row': row,
                    'col': col,
                    'val': val,
                    'isGuess': isGuess
                })
            candidates.append(candidate)

        return candidates

    # Get row and col indexes given vector type
    def getRowAndColIndexes(self, vectorType, i, j):
        if vectorType == 'row':
            return (i, j)
        elif vectorType == 'col':
            return (j, i)
        else:
            raise Exception('Unknown vector type!')

    # Check if it has consecutive three or more zeros/ones
    def isIllegal(self, vector):
        previous = None
        streak = 0
        for x in range(len(vector)):
            current = vector[x]['val']
            if current == previous:
                streak += 1
                if streak >= 2:
                    return True
            else:
                streak = 0
            previous = current

        return False

    # Check if matrix has duplicated rows/cols
    def hasDuplicatedVectors(self, vectorType, target):
        # Get complete vectors of the same type
        sources = list(filter(
            lambda x: x[0] == vectorType, self.completeVectors)
        )
        # Nothing to compare against
        if len(sources) == 0:
            return False
        # Check target against every source
        for (v, i, m) in sources:
            for j in range(len(target)):
                (row, col) = self.getRowAndColIndexes(vectorType, i, j)
                if target[j]['val'] != self.values[row][col]:
                    return False
        return True
