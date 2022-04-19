from dataclasses import dataclass
from functools import cache
from typing import List, Optional, Iterable

from auto_name_enum import AutoNameEnum, auto
from buzz import Buzz
from attrs import
from pydantic import BaseModel


MAX_BOARD_SIZE = 8


oob = object()


class GameError(Buzz):
    pass


class Direction(AutoNameEnum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


@dataclass
class Tile(BaseModel):
    row: int
    col: int
    value: int | None = None

    def __repr__(self):
        return f"{self.value} ({self.row}, {self.col})"


class Slice:
    tiles: List[Tile]

    def __init__(self, tile_gen: Iterable[Tile]):
        self.tiles = [t for t in tile_gen]

    def __repr__(self):
        return ", ".join(str(t) for t in self.tiles)

    def __eq__(self, other: "Slice") -> bool:
        """
        Compare position of tiles in two slices.
        """
        for (s, o) in zip(self.tiles, other.tiles):
            if s.row != o.row or s.col != o.col or s.value != o.value:
                return False
        return True

    def can_mash(self) -> bool:
        values: list[int | None] = [t.value for t in self.tiles]
        seen_none = False
        for (i, val) in enumerate(values):
            if val is None:
                seen_none = True
            else:
                if seen_none is True:
                    return True
                elif i < len(self.tiles) - 1 and val == values[i + 1]:
                    return True
        return False

    def mash(self):
        values: list[int | None] = [t.value for t in self.tiles]
        i = 0
        while len(values) > 0 and i < len(values) - 1:
            if values[i] is None:
                values.pop(i)
                continue

            if values[i] == values[i + 1]:
                newval = values.pop(i)
                # Make static type checkers happy
                assert newval is not None
                values[i] = newval * 2

            i += 1

        for (i, tile) in enumerate(self.tiles):
            tile.value = values[i] if i < len(values) else None

        return self




class GameBoard:
    size: int
    grid: List[Tile]

    def __init__(self, size: int = 4):
        self.size = size
        self.grid = [Tile(row=i, col=j, value=None) for i in range(size) for j in range(size)]

    @classmethod
    def from_text(cls, text: str):

        lines = text.strip().split("\n")
        size = len(lines)
        GameError.require_condition(size >= 3, "Board is too small")
        GameError.require_condition(size <= MAX_BOARD_SIZE, "Board is too big")

        board = cls(size=size)
        for (i, line) in enumerate(lines):
            values = [v.strip()  for v in line.split(',')]
            GameError.require_condition(
                len(values) == size,
                f"Wrong number of values on line {i + 1}",
            )
            for (j, value) in enumerate(values):
                if value == "":
                    value = None
                else:
                    # TODO: check for powers of 2
                    with GameError.handle_errors(f"Invalid tile value: {value}"):
                        value = int(value)
                board.grid[board.idx(i, j)].value = value


    @cache
    def idx(self, row: int, col: int) -> int:
        return row * self.size + col

    def slice(self, direction: Direction) -> Iterable[Slice]:
        up_range = range(self.size)
        down_range = range(self.size - 1, -1, -1)

        if direction is Direction.EAST:
            for i in up_range:
                yield Slice(self.grid[self.idx(i, j)] for j in down_range)

        if direction is Direction.WEST:
            for i in up_range:
                yield Slice(self.grid[self.idx(i, j)] for j in up_range)

        if direction is Direction.NORTH:
            for j in up_range:
                yield Slice(self.grid[self.idx(i, j)] for i in up_range)

        if direction is Direction.SOUTH:
            for j in up_range:
                yield Slice(self.grid[self.idx(i, j)] for i in down_range)

    # typehint for generator
    # def march(self, direction: Direction):

    #     if direction is Direction.EAST:
    #         pos_iter = (Position(row=i, col=j) for j in down_range for i in down_range)
    #     elif direction is Direction.WEST:
    #         pos_iter = (Position(row=i, col=j) for j in up_range for i in up_range)
    #     elif direction is Direction.SOUTH:
    #         pos_iter = (Position(row=i, col=j) for i in down_range for j in down_range)
    #     elif direction is Direction.NORTH:
    #         pos_iter = (Position(row=i, col=j) for i in up_range for j in up_range)
    #     else:
    #         raise GameError(f"Invalid direction: {direction}")

    #     for pos in pos_iter:
    #         yield pos
