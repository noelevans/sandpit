import numpy as np
import time
import unicornhat as hat


LINES = ['central',  'circle',
         'jubilee',  'metropolitan',
         'northern', 'piccadilly',
         'central',  'central',
         'central',  'central',
         'central',  'central',
         'central',  'central',
         'central',  'central',
        ]


def binary_to_rgb(binary, line):
    line_colours = {
        'central':      (220,  36,  31),
        'circle':       (255, 211,  41),
        'jubilee':      (161, 165, 167),
        'metropolitan': (155,   0,  88),
        'northern':     (  0,   0,   0),
        'piccadilly':   (  0,  25, 168),
    }
    dark = ['northern', 'metropolitan']
    opposites = {}
    for line in line_colours:
        opposites[line] = (0, 0, 0) if line not in dark else (230, 230, 230)
    return [b and line_colours[line] or opposites[line] for b in binary]


def layout(statuses):
    result = []
    for line in LINES:
        illuminate = {
            'good': [1, 1, 1, 1],
            'ok':   [0, 0, 1, 1],
            'bad':  [0, 0, 0, 1],
        }[statuses[line]]

        result.extend(binary_to_rgb(illuminate, line))

    return np.array(result).reshape(8, 8, 3)


def main():
    hat.set_layout(hat.AUTO)
    hat.rotation(180)
    hat.brightness(0.5)
    width, height = hat.get_shape()

    import random
    statuses = {line: random.choice(['ok']) for line in LINES}

    status = layout(statuses)
    for h in range(height):
        for w in range(width):
            hat.set_pixel(w, h, *status[w, h])
    hat.show()

    time.sleep(5)


if __name__ == '__main__':
    main()
