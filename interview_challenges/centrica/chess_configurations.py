import copy


class Board:
    __slots__ = ["columns", "rows", "positions"]

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
        if new_piece and set.intersection(
            set(new_piece.moves(position, self)), self.positions
        ):
            return False
        return True

    @classmethod
    def _copy(cls, board):
        dupe = cls(board.columns, board.rows)
        dupe.positions = copy.copy(board.positions)
        return dupe

    def place(self, position, piece):
        if position not in self.positions:
            new_board = self._copy(self)
            new_board.positions[position] = piece
            return new_board

    def __hash__(self):
        # Using sets to omit duplicate boards (2 Kings on same square
        # are equal) hence __hash__ implementation
        return sum(
            [
                37 * self.columns,
                37 * self.rows,
                37 * sum(hash(k) for k in self.positions.keys()),
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


class Piece:
    def _vector(self, board, x, y, xp, yp):
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

    def __hash__(self):
        return hash(type(self).__name__)

    def __repr__(self):
        return type(self).__name__


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


def _all_coords(board):
    return {
        (n % board.columns, n // board.rows) for n in range(board.rows * board.columns)
    }


def _potential_positions(empty_board, pieces):
    positions = {}
    for piece in set(pieces):
        free_positions = {}
        for piece_coord in _all_coords(empty_board):
            board = empty_board.place(piece_coord, piece)
            free_cells = {
                coord for coord in _all_coords(board) if board.free(coord, None)
            }
            free_positions[piece_coord] = free_cells
        positions[piece] = free_positions
    return positions


def configurations(pieces, original_board):
    potential_positions = _potential_positions(original_board, pieces)
    boards_to_free_spaces = {original_board: _all_coords(original_board)}
    for piece in pieces:
        new_boards = {}
        for board, free_spaces in boards_to_free_spaces.items():
            for free_space in free_spaces:
                if board.free(free_space, piece):
                    new_board = board.place(free_space, piece)
                    new_boards[new_board] = set.intersection(
                        potential_positions[piece][free_space], free_spaces
                    )
            boards_to_free_spaces = new_boards
    return boards_to_free_spaces


if __name__ == "__main__":
    configurations(
        [King(), King(), Queen(), Bishop(), Rook(), Knight()],
        Board(6, 9),
    )
