"""
Read in files transport_lines.txt.

Handle these cases carefully:

    More or less than 8 lines

"""

def typo_correct(input):
    subs = {
        'hamm': 'hammersmith-city',
        'over': 'overground',
        'rail': 'tflrail',
        'doc':  'dlr',
        'met':  'metropolitan',
        'pic':  'piccadilly',
        'tfl':  'tflrail',
        'wat':  'waterloo-city',
    }
    for k, v in subs.items():
        if input.startswith(k):
            return v
    return input


def main():
    lines = []
    with open('transport_lines.txt') as ol:
        for el in ol.readlines():
            text = el.strip().replace('\n', '').replace('\r', '').lower()
            line = typo_correct(text)
            lines.append(line)

    return lines[:8]


if __name__ == '__main__':
    main()
