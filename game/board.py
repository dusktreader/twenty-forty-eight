from functools import cache
from random import choice, random
from typing import List, Optional, Iterable, Any

import snick
import typer
from auto_name_enum import AutoNameEnum, NoMangleMixin, auto
from buzz import Buzz
from pydantic import BaseModel
from rich.panel import Panel
from textual.app import App
from textual.views import GridView
from textual.reactive import Reactive
from textual.widget import Widget

MAX_BOARD_SIZE = 8
MIN_BOARD_SIZE = 8
DEFAULT_BOARD_SIZE = 4


oob = object()


class GameError(Buzz):
    pass


class BadMoveError(Buzz):
    pass


class GameOverError(Buzz):
    pass


class Direction(AutoNameEnum, NoMangleMixin):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Position(BaseModel):
    row: int
    col: int

    @classmethod
    def make(cls, row: int, col: int) -> "Position":
        return cls(row=row, col=col)

class Tile(BaseModel):
    pos: Position
    value: int | None = None

    @classmethod
    def make(cls, row: int, col: int, value: int | None = None) -> "Tile":
        return cls(pos=Position.make(row, col), value=value)


class Move(BaseModel):
    start_pos: Position
    final_pos: Position
    start_value: int
    final_value: int


class Slice(BaseModel):
    tiles: list[Tile]

    @classmethod
    def make(cls, *tiles: Tile) -> "Slice":
        return cls(tiles=tiles)

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

    def mash(self) -> int:
        values: list[int | None] = [t.value for t in self.tiles]
        score = 0
        i = 0
        while len(values) > 0 and i < len(values) - 1:
            if values[i] is None:
                values.pop(i)
                continue

            if values[i + 1] is None:
                values.pop(i + 1)
                continue

            if values[i] == values[i + 1]:
                newval = values.pop(i)
                # Make static type checkers happy
                assert newval is not None
                newval = newval * 2
                score += newval
                values[i] = newval

            i += 1
        for (i, tile) in enumerate(self.tiles):
            tile.value = values[i] if i < len(values) else None

        return score


class GameBoard(BaseModel):
    size: int
    grid: list[Tile] = []
    score: int = 0

    def reset(self, should_sprinkle=True):
        self.score = 0
        self.grid = [Tile.make(i, j, value=None) for i in range(self.size) for j in range(self.size)]
        if should_sprinkle:
            self.sprinkle()
            self.sprinkle()

    @classmethod
    def from_text(cls, text: str):
        cls.parse_raw(text)

        lines = text.strip().split("\n")
        size = len(lines)
        GameError.require_condition(size >= 3, "Board is too small")
        GameError.require_condition(size <= MAX_BOARD_SIZE, "Board is too big")

        board = cls(size=size)
        board.build()
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
                board.tile(i, j).value = value

    def tile(self, row: int, col: int) -> Tile:
        return self.grid[idx(self.size, row, col)]

    def slice(self, direction: Direction) -> Iterable[Slice]:
        assert self.grid is not None
        up_range = range(self.size)
        down_range = range(self.size - 1, -1, -1)

        if direction is Direction.EAST:
            for i in up_range:
                yield Slice(tiles=[self.tile(i, j) for j in down_range])

        elif direction is Direction.WEST:
            for i in up_range:
                yield Slice(tiles=[self.tile(i, j) for j in up_range])

        elif direction is Direction.NORTH:
            for j in up_range:
                yield Slice(tiles=[self.tile(i, j) for i in up_range])

        elif direction is Direction.SOUTH:
            for j in up_range:
                yield Slice(tiles=[self.tile(i, j) for i in down_range])

    def pretty(self):
        max_val = max(self.grid, key=lambda t: t.value if t.value is not None else 0)
        digits = len(str(max_val.value))
        padding = "  "
        width = digits * self.size + len(padding) * (self.size) + 2
        output = "╔" + ("═" * width) + "╗\n"
        for i in range(self.size):
            output += f"║{padding}"
            for j in range(self.size):
                val = self.tile(i, j).value
                if val is None:
                    val = " " * digits
                else:
                    val = f"{val:{digits}}"
                output += f"{val}{padding}"
            output += "║\n"
        output += "╚" + ("═" * width) + "╝\n"
        return output

    def has_move(self) -> bool:
        return any(self.can_mash(d) for d in Direction)

    def can_mash(self, direction: Direction) -> bool:
        # TODO: Make board hashable so we can cash self.slice()?
        return any(s.can_mash() for s in self.slice(direction))

    def mash(self, direction: Direction) -> int:
        return sum(s.mash() for s in self.slice(direction))

    def sprinkle(self):
        empty_tiles = [t for t in self.grid if t.value is None]
        picked_tile = choice(empty_tiles)
        picked_tile.value = 2 if random() < 0.9 else 4

    def move(self, direction: Direction):
        BadMoveError.require_condition(
            self.can_mash(direction),
            f"Can't move {direction}",
        )
        self.score += self.mash(direction)
        self.sprinkle()
        GameOverError.require_condition(
            self.has_move(),
            "Game Over! (No moves left)"
        )


class Status(Widget):

    score = Reactive(0)
    turn = Reactive(0)
    message = Reactive("")

    def render(self):
        parts = [
            f"Score: {self.score}",
            f"Turn:  {self.turn}",
        ]
        if self.message:
            parts.extend([
                "",
                self.message,
            ])

        return Panel(snick.dedent_all(*parts))


class TuiTile(Widget):

    value = Reactive(None)

    def render(self):
        if self.value is None:
            return ""
        # TODO: actually calculate the width needed here
        return Panel(f"{self.value: ^6}")


class TuiBoard(GridView):
    board: GameBoard
    turn = Reactive(0)
    game_over = Reactive(False)

    def __init__(self, size: int, *args, **kwargs):
        self.board = GameBoard(size=size)
        self.board.reset()
        super().__init__(*args, **kwargs)

    def watch_game_over(self, value: bool):
        self.log(f"Game over!")
        if self.status is not None and value is True:
            self.status.message = "Game Over! (no moves left)"

    def watch_turn(self, value: int):
        self.log(f"reacted to change in turn: {value}")
        if self.tui_tiles is not None:
            for (i, tile) in enumerate(self.board.grid):
                self.tui_tiles[i].value = tile.value

        if self.status is not None:
            self.status.score = self.board.score
            self.status.turn = value

    def mash(self, direction: Direction):
        if self.game_over:
            return
        self.log(f"Called mash with {direction}")
        try:
            self.board.move(direction)
            self.turn += 1
            self.status.message = ""
        except GameOverError:
            self.game_over = True
            self.log("That's it, man! Game over, man! Game OVER!")
        except Exception as err:
            self.status.message = str(err)

    def on_mount(self) -> None:

        self.grid.add_column("col", max_size=10, repeat=self.board.size)
        self.grid.add_row("row", max_size=4, repeat=self.board.size)
        self.grid.add_row("status", max_size=8)

        self.grid.add_areas(status=f"col1-start|col{self.board.size}-end,status")

        self.tui_tiles = [TuiTile() for _ in self.board.grid]
        self.status = Status()
        self.game_over = False

        self.grid.place(*self.tui_tiles, status=self.status)
        self.turn = 1


@cache
def idx(size: int, row: int, col: int) -> int:
    return row * size + col


class Game(App):
    tui_board: TuiBoard

    def __init__(self, *args, size: int = DEFAULT_BOARD_SIZE, **kwargs):
        self.size = size
        super().__init__(*args, **kwargs)

    async def on_load(self, event):
        await self.bind("w", f"mash('{Direction.NORTH}')")
        await self.bind("up", f"mash('{Direction.NORTH}')")
        await self.bind("s", f"mash('{Direction.SOUTH}')")
        await self.bind("down", f"mash('{Direction.SOUTH}')")
        await self.bind("a", f"mash('{Direction.WEST}')")
        await self.bind("left", f"mash('{Direction.WEST}')")
        await self.bind("d", f"mash('{Direction.EAST}')")
        await self.bind("right", f"mash('{Direction.EAST}')")

    async def action_mash(self, dir_str: str):
        self.log(f"Got an action mash of {dir_str}")
        self.tui_board.mash(Direction[dir_str])

    async def on_mount(self) -> None:
        self.tui_board = TuiBoard(self.size)
        await self.view.dock(self.tui_board)


cli = typer.Typer()


@cli.command()
def play(
    size: int = typer.Option(
        DEFAULT_BOARD_SIZE,
        help="The size of the board (size x size).",
    ),
):
    """
    Play 2048 with the size of board you specify.

    The game is still pretty rough, but you can still have some fun.

    Animation and color coming soon.
    """
    Game.run(title="twenty-forty-eight", log="twenty-forty-eight.log", size=size)


if __name__ == '__main__':
    cli()
