#!/usr/bin/env python3


class Combo:

    def __init__(self, maxSize=5):
        self.maxSize = maxSize

    def getMaxSize(self):
        return self.maxSize

    # Get all combination given missing number of zeros and ones
    def get(count, size, vectorType, i, missingCount):
        if missingCount == 2:
            if count[vectorType][i][0] == 1:
                # One zero and one one, no doubt
                return [
                    (0, 1),
                    (1, 0)
                ]
        elif missingCount == 3:
            if count[vectorType][i][0] == size/2 - 1:
                # One zero and two ones
                return [
                    (1, 1, 0),
                    (1, 0, 1),
                    (0, 1, 1)
                ]
            elif count[vectorType][i][1] == size/2 - 1:
                # One one and two zeros
                return [
                    (0, 0, 1),
                    (0, 1, 0),
                    (1, 0, 0)
                ]
        elif missingCount == 4:
            if count[vectorType][i][0] == size/2 - 1:
                # One zero and three ones
                return [
                    (1, 1, 1, 0),
                    (1, 1, 0, 1),
                    (1, 0, 1, 1),
                    (0, 1, 1, 1)
                ]
            elif count[vectorType][i][0] == size/2 - 2:
                # Two zeros and two ones
                return [
                    (0, 0, 1, 1),
                    (0, 1, 0, 1),
                    (0, 1, 1, 0),
                    (1, 1, 0, 0),
                    (1, 0, 1, 0),
                    (1, 0, 0, 1)
                ]
            elif count[vectorType][i][1] == size/2 - 1:
                # One one and three zeros
                return [
                    (0, 0, 0, 1),
                    (0, 0, 1, 0),
                    (0, 1, 0, 0),
                    (1, 0, 0, 0)
                ]
        elif missingCount == 5:
            if count[vectorType][i][0] == 1:
                # One zero and four ones:
                return [
                    (0, 1, 1, 1, 1),
                    (1, 0, 1, 1, 1),
                    (1, 1, 0, 1, 1),
                    (1, 1, 1, 0, 1),
                    (1, 1, 1, 1, 0)
                ]
            elif count[vectorType][i][1] == 1:
                # One one and four zeros:
                return [
                    (1, 0, 0, 0, 0),
                    (0, 1, 0, 0, 0),
                    (0, 0, 1, 0, 0),
                    (0, 0, 0, 1, 0),
                    (0, 0, 0, 0, 1)
                ]

        return []
