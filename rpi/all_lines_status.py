import numpy as np
import requests
import time
import unicornhat


LINES = ['central',  'circle',
         'central',  'circle',
         'jubilee',  'metropolitan',
         'jubilee',  'metropolitan',
         'northern', 'piccadilly',
         'northern', 'piccadilly',
        ]

STATUSES = {'Good Service': 'good',
            'Minor Delays': 'ok'}   # All other statuses are 'bad'


def binary_to_rgb(binary, line):
    line_colours = {
        'central':      (220,  36,  31),
        'circle':       (255, 211,  41),
        'jubilee':      (161, 165, 167),
        'metropolitan': (155,   0,  88),
        'northern':     (  0,   0,   0),
        'piccadilly':   (  0,  25, 168),
    }
    blank = (0, 0, 0)
    return [b and line_colours.get(line, blank) or blank for b in binary]


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
    requests.packages.urllib3.disable_warnings()
    resp = requests.get('http://api.tfl.gov.uk/Line/Mode/tube/Status').json()

    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in resp}
    return {line: STATUSES.get(statuses[line], 'bad')
            for line in statuses.keys()
            if line in LINES}


def update_hat(tube_status, hat):
    hat.set_layout(hat.AUTO)
    hat.rotation(180)
    hat.brightness(0.5)
    width, height = hat.get_shape()

    weather_status = np.zeros(4 * 4 * 3).reshape(16, 3).astype(int)
    status = np.concatenate([tube_status, weather_status])
    pixel_statuses = status.reshape(width, height, 3)

    for h in range(height):
        for w in range(width):
            hat.set_pixel(h, w, *pixel_statuses[w, h])
    hat.show()


def main():
    status = layout(tube_statuses())
    update_hat(status, unicornhat)
    time.sleep(5)


if __name__ == '__main__':
    main()
