import collections
import lichess.api


def games(account, speed=None):
    return (
        g
        for g in lichess.api.user_games(account)
        if speed is None or g["speed"] == speed
    )


def player(game, color):
    return game["players"][color]["user"]["id"]


def winner(game):
    return player(game, game["winner"])


def player_moves(game, account):
    is_white = account == player(game, "white")
    start = 0 if is_white else 1
    return game["moves"].split()[start::2]


def best_openings(account, speed=None):
    openings = collections.defaultdict(lambda: [])
    for game in games(account, speed):
        first_move = player_moves(game, account)[0]
        won = winner(game) == account
        openings[first_move].append(won)
    return {
        move: f"{sum(results)} / {len(results)}" for move, results in openings.items()
    }


def run():
    account = "nudge_vans"
    speed = "correspondence"
    print(
        dict(
            (
                sorted(
                    best_openings(account, speed).items(),
                    key=lambda x: eval(x[1]),
                    reverse=True,
                )
            )
        )
    )


if __name__ == "__main__":
    run()
