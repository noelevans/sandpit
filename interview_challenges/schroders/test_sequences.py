import pytest

from sequences import Board, sequences


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            (0, 0),
            [
                (1, 2),
                (2, 1),
            ],
        ),
        (
            (2, 2),
            [
                (1, 0),
                (3, 0),
                (0, 1),
                (4, 1),
            ],
        ),
    ],
)
def test_knight_moves(inputs, expected):
    assert sorted(list(Board(inputs).moves())) == sorted(expected)


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            2,
            [
                "NC",
                "IB",
                "2I",
                "DO",
                "KB",
                "I2",
                "LC",
                "NE",
                "DG",
                "2G",
                "AH",
                "1H",
                "KH",
                "HA",
                "FC",
                "N1",
                "NG",
                "1N",
                "MD",
                "MF",
                "FM",
                "3L",
                "HE",
                "2O",
                "OD",
                "EN",
                "JC",
                "DM",
                "G2",
                "K2",
                "1F",
                "2K",
                "H1",
                "CN",
                "H3",
                "CL",
                "BK",
                "GD",
                "HO",
                "AL",
                "OH",
                "3J",
                "MJ",
                "CJ",
                "BM",
                "BI",
                "MB",
                "GN",
                "CF",
                "F1",
                "J3",
                "O2",
                "L3",
                "3H",
                "JM",
                "EH",
                "LI",
                "IL",
                "HK",
                "LA",
            ],
        ),
    ],
)
def test_sequences(inputs, expected):
    assert sorted(sequences(inputs)) == sorted(expected)


def test_only_2_vowels():
    board = Board((2, 3))
    board.path = "O2O2"
    next_boards = [board.move(m) for m in board.moves()]
    assert sorted([b.path for b in next_boards if b]) == sorted(["O2O2K", "O2O2G"])
