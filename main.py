#!/usr/bin/env python3

from Puzzle import Puzzle


puzzle = Puzzle()
puzzle.set(
    Puzzle.DIFFICULTY['medium'],
    Puzzle.LEVEL[1],
    Puzzle.SIZE['10*10']
)
puzzle.play()
