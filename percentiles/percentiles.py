import random
import statistics
import time


def percentiles(arr, centiles):
    length = len(list(arr))
    indices = [int(c * length) for c in centiles]
    for i in indices:
        return _indices(arr, i)


def _indices(arr, index):
    before = []
    after = []
    same = 0
    pivot = arr[0]
    for el in arr[1:]:
        if el < pivot:
            before.append(el)
        elif el > pivot:
            after.append(el)
        else:
            same = same + 1
    if len(before) == index:  # or index < len(before) + same:
        return pivot
    elif index < len(before):
        portion = before
        offset = index
    else:
        portion = after
        offset = index - len(before) - same - 1
    return _indices(portion, offset)


def run(min_scale, max_scale):
    random.seed(0)
    samples = [list(range(10 ** x)) for x in range(min_scale, max_scale)]
    for sample in samples:
        random.shuffle(sample)
        start = time.time()
        _ = statistics.median(sample)
        print(f"For {len(sample)} samples: {time.time() - start:.2f}s")


if __name__ == "__main__":
    # run(4, 8)
    ol = list(range(100, 191))
    random.seed(0)
    random.shuffle(ol)
    print(percentiles(ol, [0.5]))  # == 14
    # for n in range(50):
    #     ol.append(101)
    # print(percentiles(ol, [0.5]))
