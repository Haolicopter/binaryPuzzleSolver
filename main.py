#!/usr/bin/env python3

from Puzzle import Puzzle


puzzle = Puzzle()
puzzle.setLevel(
    Puzzle.DIFFICULTY['hard'],
    Puzzle.LEVEL[1],
    Puzzle.SIZE['12*12'])
puzzle.printLevel()
puzzle.play()
