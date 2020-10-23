import argparse
import functools
import io
import multiprocessing
from typing import Iterator, TextIO

"""Censor a document of words passed in a separate text file.

Pass a file path for words to be removed and a second path which
is to be censored.

Usage:
    python censor.py banned_words.txt prose.txt
"""


def censor_line(banned_words: {str}, line: str) -> Iterator[str]:
    """Removes censored words from a string.

    Args:
        banned_words: Words to be removed.
        line: String of text to be censored.
    """
    result = (word in banned_words and "*" * len(word) or word for word in line.split())
    return " ".join(result)


def run(censor_file: TextIO, prose_file: TextIO):
    """Replaces banned words with asteriks characters.

    Args:
        censor_file: File of words to be removed.
        prose_file: File to be censored.
    """
    censored_words = set(
        element.replace("\n", "") for element in censor_file.readlines()
    )
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        part = functools.partial(censor_line, censored_words)
        for line in pool.map(part, prose_file):
            print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Obscure censored words from a body of text"
    )
    parser.add_argument(
        "censored_words", type=str, help="Text file containing censored words"
    )
    parser.add_argument("body_of_text", type=str, help="Text file to be censored")
    args = parser.parse_args()

    run(open(args.censored_words), open(args.body_of_text))
