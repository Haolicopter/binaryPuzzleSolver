#!/usr/bin/env python3

from Puzzle import Puzzle


puzzle = Puzzle()
puzzle.setLevel(
    Puzzle.DIFFICULTY['medium'],
    Puzzle.LEVEL[1],
    Puzzle.SIZE['14*14'])
puzzle.printLevel()
puzzle.play()
