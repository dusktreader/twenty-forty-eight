import pytest

from game.board import Direction, Tile, Slice, GameBoard

@pytest.mark.parametrize(
    "slc,expected",
    [
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=8),
            ]),
            False,
        ),
        (
            Slice([
                Tile(row=0, col=0, value=8),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=8),
            ]),
            False,
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=2),
                Tile(row=2, col=0, value=8),
            ]),
            True,
        ),
        (
            Slice([
                Tile(row=0, col=0, value=8),
                Tile(row=1, col=0, value=2),
                Tile(row=2, col=0, value=2),
            ]),
            True,
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=None),
            ]),
            False,
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=None),
                Tile(row=2, col=0, value=None),
            ]),
            False,
        ),
        (
            Slice([
                Tile(row=0, col=0, value=None),
                Tile(row=1, col=0, value=None),
                Tile(row=2, col=0, value=None),
            ]),
            False,
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=None),
                Tile(row=2, col=0, value=8),
            ]),
            True,
        ),
        (
            Slice([
                Tile(row=0, col=0, value=None),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=8),
            ]),
            True,
        ),
    ]
)
def test_can_mash(slc: Slice, expected: bool):
    assert slc.can_mash() is expected


@pytest.mark.parametrize(
    "slc,expected",
    [
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=8),
            ]),
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=8),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=8),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=8),
            ]),
            Slice([
                Tile(row=0, col=0, value=8),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=8),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=2),
                Tile(row=2, col=0, value=8),
            ]),
            Slice([
                Tile(row=0, col=0, value=4),
                Tile(row=1, col=0, value=8),
                Tile(row=2, col=0, value=None),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=8),
                Tile(row=1, col=0, value=2),
                Tile(row=2, col=0, value=2),
            ]),
            Slice([
                Tile(row=0, col=0, value=8),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=None),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=None),
            ]),
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=None),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=None),
                Tile(row=2, col=0, value=8),
            ]),
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=8),
                Tile(row=2, col=0, value=None),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=None),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=8),
            ]),
            Slice([
                Tile(row=0, col=0, value=4),
                Tile(row=1, col=0, value=8),
                Tile(row=2, col=0, value=None),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=2),
                Tile(row=2, col=0, value=4),
                Tile(row=3, col=0, value=4),
            ]),
            Slice([
                Tile(row=0, col=0, value=4),
                Tile(row=1, col=0, value=8),
                Tile(row=2, col=0, value=None),
                Tile(row=3, col=0, value=None),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=2),
                Tile(row=2, col=0, value=2),
                Tile(row=3, col=0, value=2),
            ]),
            Slice([
                Tile(row=0, col=0, value=4),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=None),
                Tile(row=3, col=0, value=None),
            ]),
        ),
        (
            Slice([
                Tile(row=0, col=0, value=2),
                Tile(row=1, col=0, value=2),
                Tile(row=2, col=0, value=4),
                Tile(row=3, col=0, value=2),
                Tile(row=4, col=0, value=2),
            ]),
            Slice([
                Tile(row=0, col=0, value=4),
                Tile(row=1, col=0, value=4),
                Tile(row=2, col=0, value=4),
                Tile(row=3, col=0, value=None),
                Tile(row=4, col=0, value=None),
            ]),
        ),
    ]
)
def test_mash(slc: Slice, expected: Slice):
    assert slc.mash() == expected


@pytest.mark.parametrize(
    "size,direction,expected",
    [
        (
            3,
            Direction.NORTH,
            [
                Slice([
                    Tile(row=0, col=0),
                    Tile(row=1, col=0),
                    Tile(row=2, col=0),
                ]),
                Slice([
                    Tile(row=0, col=1),
                    Tile(row=1, col=1),
                    Tile(row=2, col=1),
                ]),
                Slice([
                    Tile(row=0, col=2),
                    Tile(row=1, col=2),
                    Tile(row=2, col=2),
                ]),
            ],
        ),
        (
            3,
            Direction.SOUTH,
            [
                Slice([
                    Tile(row=2, col=0),
                    Tile(row=1, col=0),
                    Tile(row=0, col=0),
                ]),
                Slice([
                    Tile(row=2, col=1),
                    Tile(row=1, col=1),
                    Tile(row=0, col=1),
                ]),
                Slice([
                    Tile(row=2, col=2),
                    Tile(row=1, col=2),
                    Tile(row=0, col=2),
                ]),
            ],
        ),
        (
            3,
            Direction.EAST,
            [
                Slice([
                    Tile(row=0, col=2),
                    Tile(row=0, col=1),
                    Tile(row=0, col=0),
                ]),
                Slice([
                    Tile(row=1, col=2),
                    Tile(row=1, col=1),
                    Tile(row=1, col=0),
                ]),
                Slice([
                    Tile(row=2, col=2),
                    Tile(row=2, col=1),
                    Tile(row=2, col=0),
                ]),
            ],
        ),
        (
            3,
            Direction.WEST,
            [
                Slice([
                    Tile(row=0, col=0),
                    Tile(row=0, col=1),
                    Tile(row=0, col=2),
                ]),
                Slice([
                    Tile(row=1, col=0),
                    Tile(row=1, col=1),
                    Tile(row=1, col=2),
                ]),
                Slice([
                    Tile(row=2, col=0),
                    Tile(row=2, col=1),
                    Tile(row=2, col=2),
                ]),
            ],
        ),
    ],
)
def test_slice(size, direction, expected):
    board = GameBoard(size=size)
    computed = list(board.slice(direction))
    assert all(c == e for (c, e) in zip(computed, expected))


# @pytest.mark.parametrize(
#     "size,direction,expected",
#     [
#         (
#             3,
#             Direction.NORTH,
#             [
#                 Position(row=0, col=0),
#                 Position(row=0, col=1),
#                 Position(row=0, col=2),
#                 Position(row=1, col=0),
#                 Position(row=1, col=1),
#                 Position(row=1, col=2),
#                 Position(row=2, col=0),
#                 Position(row=2, col=1),
#                 Position(row=2, col=2),
#             ],
#         ),
#         (
#             3,
#             Direction.SOUTH,
#             [
#                 Position(row=2, col=2),
#                 Position(row=2, col=1),
#                 Position(row=2, col=0),
#                 Position(row=1, col=2),
#                 Position(row=1, col=1),
#                 Position(row=1, col=0),
#                 Position(row=0, col=2),
#                 Position(row=0, col=1),
#                 Position(row=0, col=0),
#             ],
#         ),
#         (
#             3,
#             Direction.WEST,
#             [
#                 Position(row=0, col=0),
#                 Position(row=1, col=0),
#                 Position(row=2, col=0),
#                 Position(row=0, col=1),
#                 Position(row=1, col=1),
#                 Position(row=2, col=1),
#                 Position(row=0, col=2),
#                 Position(row=1, col=2),
#                 Position(row=2, col=2),
#             ],
#         ),
#         (
#             3,
#             Direction.EAST,
#             [
#                 Position(row=2, col=2),
#                 Position(row=1, col=2),
#                 Position(row=0, col=2),
#                 Position(row=2, col=1),
#                 Position(row=1, col=1),
#                 Position(row=0, col=1),
#                 Position(row=2, col=0),
#                 Position(row=1, col=0),
#                 Position(row=0, col=0),
#             ],
#         ),
#     ],
# )
# def test_march(size, direction, expected):
#     board = GameBoard(size=size)
#     assert list(board.march(direction)) == expected
