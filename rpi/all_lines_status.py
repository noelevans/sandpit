import numpy as np
import time
import unicornhat


LINES = ['central',  'circle',
         'central',  'circle',
         'jubilee',  'metropolitan',
         'jubilee',  'metropolitan',
         'northern', 'piccadilly',
         'northern', 'piccadilly',
         '',         '',
         '',         '',
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
    return [line_colours.get(line, (0, 0, 0)) for b in binary]


def layout(statuses):
    result = []
    for line in LINES:
        illuminate = {
            'good': [1, 1, 1, 1],
            'ok':   [0, 0, 1, 1],
            'bad':  [0, 0, 0, 1],
        }[statuses[line]]

        result.extend(binary_to_rgb(illuminate, line))

    return np.array(result)


def tube_statuses():
    import random
    return {line: random.choice(['bad', 'good', 'ok']) for line in LINES}


def update_hat(status, hat):
    hat.set_layout(hat.AUTO)
    hat.rotation(270)
    hat.brightness(0.5)
    width, height = hat.get_shape()
    pixel_statuses = status.reshape(width, height, 3)

    for h in range(height):
        for w in range(width):
            hat.set_pixel(w, h, *status[w, h])
    hat.show()


def main():
    status = layout(tube_statuses())
    update_hat(status, unicornhat)
    time.sleep(5)


if __name__ == '__main__':
    main()
