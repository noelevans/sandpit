import copy
import itertools


class Board:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.positions = {}

    def free(self, position, new_piece):
        if position in self.positions:
            return False
        for occupied_position, piece in self.positions.items():
            if position in piece.moves(occupied_position, self):
                return False
        if set.intersection(set(new_piece.moves(position, self)), self.positions):
            return False
        return True

    @classmethod
    def _copy(cls, board):
        dupe = cls(board.columns, board.rows)
        dupe.positions = copy.copy(board.positions)
        return dupe

    def place(self, position, piece):
        new_board = self._copy(self)
        new_board.positions[position] = piece
        return new_board

    def __hash__(self):
        # As we are using sets to omit duplicate boards (2 Kings on same
        # square are equal) we need to implement __hash__
        return sum(
            [
                39 * self.columns,
                39 * self.rows,
                39 * sum(hash(k) for k in self.positions.keys()),
            ]
        )

    def __eq__(self, other):
        if (
            self.columns != other.columns
            or self.rows != other.rows
            or len(self.positions) != len(other.positions)
        ):
            return False
        for sp, op in zip(sorted(self.positions), sorted(other.positions)):
            if sp != op or self.positions[sp] != other.positions[op]:
                return False
        return True

    def __str__(self):
        result = []
        for x in range(self.columns):
            portion = []
            for y in range(self.rows):
                if (x, y) in self.positions:
                    portion.append(self.positions[(x, y)].__class__.__name__[0])
                else:
                    portion.append(" ")
            result.append("|".join(portion))

        return "\n".join(result)

    def __repr__(self):
        return self.__str__()


class Piece:
    def _vector(self, board, x, y, xp, yp):
        stop = False
        while (0 <= (x + xp) < board.columns) and (0 <= (y + yp) < board.rows):
            yield x + xp, y + yp
            x += xp
            y += yp

    def straight_moves(self, position, board):
        yield from self._vector(board, *position, 0, +1)
        yield from self._vector(board, *position, 0, -1)
        yield from self._vector(board, *position, +1, 0)
        yield from self._vector(board, *position, -1, 0)

    def diagonal_moves(self, position, board):
        yield from self._vector(board, *position, +1, +1)
        yield from self._vector(board, *position, +1, -1)
        yield from self._vector(board, *position, -1, +1)
        yield from self._vector(board, *position, -1, -1)

    def _omit_off_board(self, positions, board):
        for position in positions:
            if 0 <= position[0] < board.columns and 0 <= position[1] < board.rows:
                yield position

    def __eq__(self, other):
        return type(self) == type(other)


class King(Piece):
    def moves(self, position, board):
        return self._omit_off_board(
            [
                (position[0] - 1, position[1]),
                (position[0] + 1, position[1]),
                (position[0], position[1] - 1),
                (position[0], position[1] + 1),
                (position[0] - 1, position[1] - 1),
                (position[0] - 1, position[1] + 1),
                (position[0] + 1, position[1] - 1),
                (position[0] + 1, position[1] + 1),
            ],
            board,
        )


class Queen(Piece):
    def moves(self, position, board):
        yield from self.diagonal_moves(position, board)
        yield from self.straight_moves(position, board)


class Bishop(Piece):
    def moves(self, position, board):
        yield from self.diagonal_moves(position, board)


class Knight(Piece):
    def moves(self, position, board):
        return self._omit_off_board(
            [
                (position[0] - 1, position[1] - 2),
                (position[0] - 1, position[1] + 2),
                (position[0] + 1, position[1] - 2),
                (position[0] + 1, position[1] + 2),
                (position[0] - 2, position[1] - 1),
                (position[0] - 2, position[1] + 1),
                (position[0] + 2, position[1] - 1),
                (position[0] + 2, position[1] + 1),
            ],
            board,
        )


class Rook(Piece):
    def moves(self, position, board):
        yield from self.straight_moves(position, board)


def _free_positions(board, piece):
    for row in range(board.rows):
        for column in range(board.columns):
            if board.free((column, row), piece):
                yield board.place((column, row), piece)


def configurations(pieces, board):
    boards = [board]
    for piece in pieces:
        next_boards = []
        for board in boards:
            next_boards.append(set(_free_positions(board, piece)))
        boards = itertools.chain(*next_boards)
    return set(boards)


if __name__ == "__main__":
    import time

    start = time.time()
    print(
        len(
            configurations(
                [Queen(), Rook(), Bishop(), King(), King(), Knight()],
                Board(6, 9),
            )
        )
    )
    print(time.time() - start)
