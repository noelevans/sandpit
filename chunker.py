"""
You have an api that returns millions of objects in a generator. This must be 
passed to another fn that only handles non-generator lists. Use something like
this too grab small chunks of the generator and feed them to the receiving fn
in small bites.
"""


def make_chunks(gen, chunk_size=1000):
    finished = False
    while not finished:
        chunk = []
        for _ in range(chunk_size):
            try:
                chunk.append(gen.next())
            except StopIteration:
                finished = True
                break
        yield chunk


def main():
    alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    for chunk in make_chunks(iter(alphabet), 7):
        for value in chunk:
            print value,
        print ""


if __name__ == "__main__":
    main()
