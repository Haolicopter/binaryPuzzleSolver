#!/usr/bin/env python3

from Puzzle import Puzzle


puzzle = Puzzle()
puzzle.set(
    Puzzle.DIFFICULTY['hard'],
    Puzzle.LEVEL[88],
    Puzzle.SIZE['14*14']
)
puzzle.play()
