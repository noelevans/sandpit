"""
Read in files transport_lines.txt.

Handle these cases carefully:

    More or less than 8 lines

"""

import colours
import time


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


def line_choices():
    lines = []
    with open('transport_lines.txt') as ol:
        for el in ol.readlines():
            text = el.strip().replace('\n', '').replace('\r', '').lower()
            line = typo_correct(text)
            lines.append(line)

    return lines[:8]


def transport_status():
    status_aliases = {'Good Service': 'GOOD',
                      'Minor Delays': 'OK'}   # All other statuses are 'BAD'
    requests.packages.urllib3.disable_warnings()
    url = ('https://api.tfl.gov.uk/Line/Mode/' +
        'tube,dlr,overground,tflrail,tram/Status')
    resp = requests.get(url).json()

    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in resp}
    return {k: status_aliases.get(statuses[k], 'BAD') for k in statuses.keys()}


def pixel_operation(status):

    def good_op(x, r, g, b):
        blinkt.set_pixel(x, r, g, b, brightness=0.2)

    def flash_op(x, r, g, b):
        while True:
            blinkt.set_pixel(x, r, g, b, brightness=0.2)
            time.sleep(1)
            blinkt.set_pixel(x, r, g, b, brightness=0.0)
            time.sleep(1)

    def off_op(x, r, g, b):
        blinkt.set_pixel(x, r, g, b, brightness=0.0)

    return {
            'GOOD': good_op,
            'OK':   flash_op,
            'BAD':  off_op,
        }[status]


def set_pixel(n, rgb, fn):
    fn(n, *rgb)


def illuminate():
    lines = line_choices()
    status = transport_status()
    line_colours = [colours.LINE_COLOURS.get(el) for el in lines]

    for n, (rgb, s) in enumerate(zip(line_colours, status)):
        set_pixel(n, rgb, pixel_operation(s))


def main():
    illuminate()
    time.sleep(10)


if __name__ == '__main__':
    main()
