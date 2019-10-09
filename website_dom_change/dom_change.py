from dataclasses import dataclass
from typing import Callable
from bs4 import BeautifulSoup
import requests


@dataclass
class Monitor:
    name: str
    url: str
    dom_obj: Callable[[str], str]


MONITORS = [
    Monitor(
        'New easy Neovim bugs',
        'https://github.com/neovim/neovim/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22',
        lambda s: s.find("div", {"id": "js-issues-toolbar"}).find('a').text,
        ),
]


def alert():
    pass


def main():
    for m in MONITORS:
        filename = m.name.replace(' ', '_').lower() + '.txt'
        old_text = open(filename).read()
        soup = BeautifulSoup(requests.get(m.url).content)
        current_text = m.dom_obj(soup)
        if old_text != current_text:
            alert(m)

        # Write to file each time to assure code is being run
        with open(filename, 'w') as f:
            f.write(current_text)


if __name__ == '__main__':
    main()
