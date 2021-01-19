class Board:
    shape = [
        ["A", "B", "C", "D", "E"],
        ["F", "G", "H", "I", "J"],
        ["K", "L", "M", "N", "O"],
        [None, "1", "2", "3", None],
    ]
    rows = len(shape)
    columns = len(shape[0])

    def __init__(self, coord, path=None):
        self.coord = coord
        self.path = path if path else ""

    @classmethod
    def cells(self):
        return {
            (x, y): cell
            for y, row in enumerate(self.shape)
            for x, cell in enumerate(row)
            if cell
        }

    def _is_legal(self):
        return sum(1 for c in self.path if c in "AEIOU") < 3

    def move(self, coord):
        dupe = self.__class__(coord, self.path)
        dupe.path = self.path + self.shape[coord[1]][coord[0]]
        if dupe._is_legal():
            return dupe

    def moves(self):
        destinations = [
            (self.coord[0] - 1, self.coord[1] - 2),
            (self.coord[0] - 1, self.coord[1] + 2),
            (self.coord[0] + 1, self.coord[1] - 2),
            (self.coord[0] + 1, self.coord[1] + 2),
            (self.coord[0] - 2, self.coord[1] - 1),
            (self.coord[0] - 2, self.coord[1] + 1),
            (self.coord[0] + 2, self.coord[1] - 1),
            (self.coord[0] + 2, self.coord[1] + 1),
        ]
        for position in destinations:
            if (
                0 <= position[0] < self.columns
                and 0 <= position[1] < self.rows
                and position not in [(0, 3), (4, 3)]
            ):
                yield position


def sequences(steps=10):
    boards = [Board(coord, value) for coord, value in Board.cells().items()]
    for n in range(steps - 1):
        new_boards = list()
        for board in boards:
            for m in board.moves():
                moved_board = board.move(m)
                if moved_board:
                    new_boards.append(moved_board)
        boards = new_boards
    return [b.path for b in boards]


if __name__ == "__main__":
    print(len(sequences(10)))
