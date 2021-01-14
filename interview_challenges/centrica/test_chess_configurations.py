import pytest
from chess_configurations import (
    King,
    Queen,
    Bishop,
    Knight,
    Rook,
    Board,
    configurations,
)


@pytest.mark.parametrize(
    "piece, expected",
    [
        (
            Bishop,
            {
                (0, 0),
                (1, 1),
                (3, 3),
                (4, 4),
                (0, 4),
                (1, 3),
                (3, 1),
                (4, 0),
            },
        ),
        (
            Queen,
            {
                (0, 0),
                (1, 1),
                (3, 3),
                (4, 4),
                (0, 4),
                (1, 3),
                (3, 1),
                (4, 0),
                (0, 2),
                (1, 2),
                (3, 2),
                (4, 2),
                (2, 0),
                (2, 1),
                (2, 3),
                (2, 4),
            },
        ),
    ],
)
def test_piece_positions(piece, expected):
    assert set(piece().moves((2, 2), Board(5, 5))) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            (
                [
                    King(),
                ],
                Board(3, 3),
            ),
            9,
        ),
        (
            (
                [
                    King(),
                    King(),
                ],
                Board(3, 3),
            ),
            16,
        ),
        (
            (
                [
                    King(),
                    King(),
                    Rook(),
                ],
                Board(3, 3),
            ),
            4,
        ),
        (
            (
                [
                    Rook(),
                    Rook(),
                    Knight(),
                    Knight(),
                    Knight(),
                    Knight(),
                ],
                Board(4, 4),
            ),
            8,
        ),
        (
            (
                [
                    Rook(),
                    Rook(),
                    Knight(),
                    Knight(),
                    Knight(),
                    Knight(),
                ],
                Board(4, 4),
            ),
            8,
        ),
        (
            (
                [
                    King(),
                    King(),
                    Queen(),
                    Bishop(),
                    Rook(),
                    Knight(),
                ],
                Board(6, 9),
            ),
            180568,
        ),
    ],
)
def test_configurations(test_input, expected):
    assert len(configurations(*test_input)) == expected
