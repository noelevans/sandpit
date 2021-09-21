import functools
import requests
import time


def token():
    with open("token.txt") as f:
        return f.read().replace("\n", "")


def pgns():
    with open("all_chess_dot_com_games.pgn") as f:
        content = "".join(f.readlines())
        return content.split("""[Event "Let's Play!"]\n""")


def run():
    url = "https://lichess.org/api/import"
    header = {"Authorization": f"Bearer {token()}"}
    for n, pgn in enumerate(pgns()):
        try:
            requests_call = functools.partial(
                requests.post(url, headers=header, data={"pgn": pgn})
            )
            response = requests_call()
            print(response.json()["url"])
        except:
            print(f"Unable to import {n}th record")
            time.sleep(120)
            response = requests_call()
            print(response.json()["url"])


if __name__ == "__main__":
    run()
