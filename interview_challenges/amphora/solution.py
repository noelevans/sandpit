import collections
import re


def histogram(text):
    words = (x.group(0).lower() for x in re.finditer(r"[\w]+", text))
    result = collections.Counter(words).most_common(10)
    for word, count in result:
        print(f"{word} {count}")


if __name__ == "__main__":
    histogram(
        "count the words in this sample text and print words count for the 10 most frequent words"
    )
