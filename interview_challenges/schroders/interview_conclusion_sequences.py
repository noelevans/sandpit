import functools


class Route:
    def __init__(self, board, coord, other_route=None):
        self.board = board
        self.vowels = int(board.shape[coord[1]][coord[0]] in "AEIOU")
        if other_route:
            self.vowels += other_route.vowels
        self.coord = coord

    def is_legal(self):
        return self.vowels < 3


class Board:
    shape = [
        ["A", "B", "C", "D", "E"],
        ["F", "G", "H", "I", "J"],
        ["K", "L", "M", "N", "O"],
        [None, "1", "2", "3", None],
    ]
    rows = len(shape)
    columns = len(shape[0])

    @classmethod
    def cells(self):
        return {
            (x, y): cell
            for y, row in enumerate(self.shape)
            for x, cell in enumerate(row)
            if cell
        }

    @functools.lru_cache(100)
    def destinations(self, coord):
        destinations = [
            (coord[0] - 1, coord[1] - 2),
            (coord[0] - 1, coord[1] + 2),
            (coord[0] + 1, coord[1] - 2),
            (coord[0] + 1, coord[1] + 2),
            (coord[0] - 2, coord[1] - 1),
            (coord[0] - 2, coord[1] + 1),
            (coord[0] + 2, coord[1] - 1),
            (coord[0] + 2, coord[1] + 1),
        ]
        return [
            position
            for position in destinations
            if (
                0 <= position[0] < self.columns
                and 0 <= position[1] < self.rows
                and self.shape[position[1]][position[0]]
            )
        ]


def sequences(steps):
    board = Board()
    routes = [Route(board, coord) for coord, _ in Board.cells().items()]
    for n in range(steps):
        new_routes = []
        for route in routes:
            for m in board.destinations(route.coord):
                moved_route = Route(board, m, route)
                if moved_route and moved_route.is_legal():
                    new_routes.append(moved_route)
        routes = new_routes
    return len(routes)


if __name__ == "__main__":
    import time

    start = time.time()
    print(sequences(9))
    print(time.time() - start)
