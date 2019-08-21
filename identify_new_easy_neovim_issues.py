import operator
import requests


def main():
    args = {"state": "open", "labels": "good+first+issue"}
    url = "http://api.github.com/repos/neovim/neovim/issues?{}".format(
        "&".join([k + "=" + v for k, v in args.items()])
    )
    resp = requests.get(url).json()
    for issue in sorted(
        resp, key=operator.itemgetter("created_at"), reverse=True
    ):
        print(issue["title"], issue["created_at"], issue["comments"])


if __name__ == "__main__":
    main()
