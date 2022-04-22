import pytest
import snick

from game.board import Direction, Tile, Slice, GameBoard


@pytest.fixture
def board_reader():
    def _helper(text: str):
        lines = text.strip().split("\n")
        size = len(lines)
        grid = []
        for (i, line) in enumerate(lines):
            values = [v.strip()  for v in line.split(',')]
            for (j, value) in enumerate(values):
                if value == "":
                    value = None
                else:
                    value = int(value)
                grid.append(Tile.make(i, j, value=value))

        return GameBoard(size=size, grid=grid)

    return _helper


@pytest.mark.parametrize(
    "slc,expected",
    [
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 8),
            ),
            False,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 8),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 8),
            ),
            False,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 2),
                Tile.make(2, 0, 8),
            ),
            True,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 8),
                Tile.make(1, 0, 2),
                Tile.make(2, 0, 2),
            ),
            True,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, None),
            ),
            False,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, None),
                Tile.make(2, 0, None),
            ),
            False,
        ),
        (
            Slice.make(
                Tile.make(0, 0, None),
                Tile.make(1, 0, None),
                Tile.make(2, 0, None),
            ),
            False,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, None),
                Tile.make(2, 0, 8),
            ),
            True,
        ),
        (
            Slice.make(
                Tile.make(0, 0, None),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 8),
            ),
            True,
        ),
    ]
)
def test_can_mash(slc: Slice, expected: bool):
    assert slc.can_mash() is expected


@pytest.mark.parametrize(
    "slc,expected,score",
    [
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 8),
            ),
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 8),
            ),
            0,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 8),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 8),
            ),
            Slice.make(
                Tile.make(0, 0, 8),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 8),
            ),
            0,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 2),
                Tile.make(2, 0, 8),
            ),
            Slice.make(
                Tile.make(0, 0, 4),
                Tile.make(1, 0, 8),
                Tile.make(2, 0, None),
            ),
            4,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 8),
                Tile.make(1, 0, 2),
                Tile.make(2, 0, 2),
            ),
            Slice.make(
                Tile.make(0, 0, 8),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, None),
            ),
            4,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, None),
            ),
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, None),
            ),
            0,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, None),
                Tile.make(2, 0, 8),
            ),
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 8),
                Tile.make(2, 0, None),
            ),
            0,
        ),
        (
            Slice.make(
                Tile.make(0, 0, None),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 8),
            ),
            Slice.make(
                Tile.make(0, 0, 4),
                Tile.make(1, 0, 8),
                Tile.make(2, 0, None),
            ),
            0,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 2),
                Tile.make(2, 0, 4),
                Tile.make(3, 0, 4),
            ),
            Slice.make(
                Tile.make(0, 0, 4),
                Tile.make(1, 0, 8),
                Tile.make(2, 0, None),
                Tile.make(3, 0, None),
            ),
            12,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 2),
                Tile.make(2, 0, 2),
                Tile.make(3, 0, 2),
            ),
            Slice.make(
                Tile.make(0, 0, 4),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, None),
                Tile.make(3, 0, None),
            ),
            8,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, 2),
                Tile.make(2, 0, 4),
                Tile.make(3, 0, 2),
                Tile.make(4, 0, 2),
            ),
            Slice.make(
                Tile.make(0, 0, 4),
                Tile.make(1, 0, 4),
                Tile.make(2, 0, 4),
                Tile.make(3, 0, None),
                Tile.make(4, 0, None),
            ),
            8,
        ),
        (
            Slice.make(
                Tile.make(0, 0, 2),
                Tile.make(1, 0, None),
                Tile.make(2, 0, 2),
                Tile.make(3, 0, None),
                Tile.make(4, 0, 2),
            ),
            Slice.make(
                Tile.make(0, 0, 4),
                Tile.make(1, 0, 2),
                Tile.make(2, 0, None),
                Tile.make(3, 0, None),
                Tile.make(4, 0, None),
            ),
            4,
        ),
    ]
)
def test_mash_slice(slc: Slice, expected: Slice, score: int):
    assert slc.mash() == score
    assert slc == expected


@pytest.mark.parametrize(
    "size,direction,expected",
    [
        (
            3,
            Direction.NORTH,
            [
                Slice.make(
                    Tile.make(0, 0),
                    Tile.make(1, 0),
                    Tile.make(2, 0),
                ),
                Slice.make(
                    Tile.make(0, 1),
                    Tile.make(1, 1),
                    Tile.make(2, 1),
                ),
                Slice.make(
                    Tile.make(0, 2),
                    Tile.make(1, 2),
                    Tile.make(2, 2),
                ),
            ],
        ),
        (
            3,
            Direction.SOUTH,
            [
                Slice.make(
                    Tile.make(2, 0),
                    Tile.make(1, 0),
                    Tile.make(0, 0),
                ),
                Slice.make(
                    Tile.make(2, 1),
                    Tile.make(1, 1),
                    Tile.make(0, 1),
                ),
                Slice.make(
                    Tile.make(2, 2),
                    Tile.make(1, 2),
                    Tile.make(0, 2),
                ),
            ],
        ),
        (
            3,
            Direction.EAST,
            [
                Slice.make(
                    Tile.make(0, 2),
                    Tile.make(0, 1),
                    Tile.make(0, 0),
                ),
                Slice.make(
                    Tile.make(1, 2),
                    Tile.make(1, 1),
                    Tile.make(1, 0),
                ),
                Slice.make(
                    Tile.make(2, 2),
                    Tile.make(2, 1),
                    Tile.make(2, 0),
                ),
            ],
        ),
        (
            3,
            Direction.WEST,
            [
                Slice.make(
                    Tile.make(0, 0),
                    Tile.make(0, 1),
                    Tile.make(0, 2),
                ),
                Slice.make(
                    Tile.make(1, 0),
                    Tile.make(1, 1),
                    Tile.make(1, 2),
                ),
                Slice.make(
                    Tile.make(2, 0),
                    Tile.make(2, 1),
                    Tile.make(2, 2),
                ),
            ],
        ),
    ],
)
def test_slice(size, direction, expected):
    board = GameBoard(size=size)
    board.reset(should_sprinkle=False)
    computed = list(board.slice(direction))
    assert all(c == e for (c, e) in zip(computed, expected))


def test_reader(board_reader):
    board = board_reader("""
        2, 4, 8
        4,  , 4
        8, 4, 2
    """)
    assert board.tile(0, 0).value == 2
    assert board.tile(0, 1).value == 4
    assert board.tile(0, 2).value == 8

    assert board.tile(1, 0).value == 4
    assert board.tile(1, 1).value == None
    assert board.tile(1, 2).value == 4

    assert board.tile(2, 0).value == 8
    assert board.tile(2, 1).value == 4
    assert board.tile(2, 2).value == 2


def test_pretty(board_reader):
    board = board_reader("""
         2,   4,   8
        16,    ,  32
        64, 128, 256
    """)
    assert board.pretty() == snick.dedent(
        """
        ╔═════════════════╗
        ║    2    4    8  ║
        ║   16        32  ║
        ║   64  128  256  ║
        ╚═════════════════╝
        """
    ) + "\n"

@pytest.mark.parametrize(
    "board_text,direction,expected",
    [
        (
            """
              2,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            Direction.NORTH,
            False,
        ),
        (
            """
              2,   4,   8
              2,  32,  64
            128, 256, 512
            """,
            Direction.NORTH,
            True,
        ),
        (
            """
              2,   4,   8
              2,  32,  64
            128, 256, 512
            """,
            Direction.SOUTH,
            True,
        ),
        (
            """
              2,   4,   8
              2,  32,  64
            128, 256, 512
            """,
            Direction.EAST,
            False,
        ),
        (
            """
               ,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            Direction.NORTH,
            True,
        ),
        (
            """
               ,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            Direction.SOUTH,
            False,
        ),
        (
            """
              2,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            Direction.NORTH,
            False,
        ),
        (
            """
               ,    ,
               ,    ,
               ,    ,
            """,
            Direction.NORTH,
            False,
        ),
        (
            """
               ,    ,
               ,    ,
               ,    ,
            """,
            Direction.WEST,
            False,
        ),
    ],
)
def test_can_mash(board_text, direction, expected, board_reader):
    board = board_reader(board_text)
    assert board.can_mash(direction) is expected


@pytest.mark.parametrize(
    "board_text,direction,expected, score",
    [
        (
            """
              2,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            Direction.NORTH,
            """
              2,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            0,
        ),
        (
            """
              2,   4,   8
              2,  32,  64
            128, 256, 512
            """,
            Direction.NORTH,
            """
              4,   4,   8
            128,  32,  64
               , 256, 512
            """,
            4,
        ),
        (
            """
              2,   4,   8
              2,  32,  64
            128, 256, 512
            """,
            Direction.SOUTH,
            """
               ,   4,   8
              4,  32,  64
            128, 256, 512
            """,
            4,
        ),
        (
            """
              2,   4,   8
              2,  32,  64
            128, 256, 512
            """,
            Direction.EAST,
            """
              2,   4,   8
              2,  32,  64
            128, 256, 512
            """,
            0,
        ),
        (
            """
               ,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            Direction.NORTH,
            """
             16,   4,   8
            128,  32,  64
               , 256, 512
            """,
            0,
        ),
        (
            """
               ,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            Direction.SOUTH,
            """
               ,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            0,
        ),
        (
            """
            2, 2, 2, 2, 2
            2, 2, 2, 2, 2
            2, 2, 2, 2, 2
            2, 2, 2, 2, 2
            2, 2, 2, 2, 2
            """,
            Direction.NORTH,
            """
            4, 4, 4, 4, 4
            4, 4, 4, 4, 4
            2, 2, 2, 2, 2
             ,  ,  ,  ,
             ,  ,  ,  ,
            """,
            40,
        ),
    ],
)
def test_mash_board(board_text, direction, expected, score, board_reader):
    board = board_reader(board_text)
    assert board.mash(direction) == score
    assert board== board_reader(expected)


@pytest.mark.parametrize(
    "board_text,expected",
    [
        (
            """
              2,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            False,
        ),
        (
            """
              2,   4,   8
              2,  32,  64
            128, 256, 512
            """,
            True,
        ),
        (
            """
               ,   4,   8
             16,  32,  64
            128, 256, 512
            """,
            True,
        ),
        (
            """
               ,    ,
               ,    ,
               ,    ,
            """,
            False,
        ),
        (
            """
              2,   4,   8
             16,    ,  64
            128, 256, 512
            """,
            True,
        ),
    ],
)
def test_has_move(board_text, expected, board_reader):
    board = board_reader(board_text)
    assert board.has_move() is expected


def test_sprinkle(mocker):
    board = GameBoard(size=3)
    board.reset(should_sprinkle=False)
    assert board.grid is not None

    mocker.patch("game.board.random", return_value=0.8)
    board.sprinkle()
    values = [t.value for t in board.grid]
    assert values.count(2) == 1
    assert values.count(4) == 0
    assert values.count(None) == 8

    mocker.patch("game.board.random", return_value=0.9)
    board.reset(should_sprinkle=False)
    board.sprinkle()
    assert board.grid is not None
    values = [t.value for t in board.grid]
    assert values.count(2) == 0
    assert values.count(4) == 1
    assert values.count(None) == 8
