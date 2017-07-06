#!/usr/bin/env python3

from Puzzle import Puzzle


puzzle = Puzzle()
puzzle.set(
    Puzzle.DIFFICULTY['very hard'],
    Puzzle.LEVEL[27],
    Puzzle.SIZE['14*14']
)
puzzle.play()
