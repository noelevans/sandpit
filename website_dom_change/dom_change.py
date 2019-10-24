from dataclasses import dataclass
from typing import Callable
from bs4 import BeautifulSoup
import requests

import email


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


def alert(name, before, after):
    email.send(name, 'Before: {}\n\nAfter: {}'.format(before, after))
    print('Email sent for {}'.format(name))


def main():
    for m in MONITORS:
        filename = m.name.replace(' ', '_').lower() + '.txt'
        try:
            old_text = open(filename).read()
        except FileNotFoundError:
            old_text = None

        soup = BeautifulSoup(requests.get(m.url).content, features='lxml')
        current_text_raw = m.dom_obj(soup)
        current_text = current_text_raw.replace('\\n', ' ').strip()

        if old_text != current_text and old_text is not None:
            alert(m.name, old_text, current_text)

        # Write to file each time to assure code is being run
        with open(filename, 'w') as f:
            f.write(current_text)


if __name__ == '__main__':
    main()
