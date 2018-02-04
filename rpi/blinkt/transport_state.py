"""
Read in files transport_lines.txt.

Handle these cases carefully:

    More or less than 8 lines

"""

import blinkt
import colours
import requests
import time


def typo_correct(input):
    subs = {
        'hamm': 'hammersmith-city',
        'over': 'london-overground',
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
        blinkt.set_pixel(x, r, g, b, brightness=0.04)

    def flash_op(x, r, g, b):
        while True:
            blinkt.set_pixel(x, r, g, b, brightness=0.04)
            blinkt.show()
            time.sleep(1)
            blinkt.set_pixel(x, r, g, b, brightness=0.0)
            blinkt.show()
            time.sleep(1)

    def off_op(x, r, g, b):
        blinkt.set_pixel(x, r, g, b, brightness=0.0)

    return {
            'GOOD': good_op,
            'OK':   flash_op,
            'BAD':  flash_op,   #off_op,
        }[status]


def illuminate():
    lines = line_choices()
    all_statuses = transport_status()
    status = [all_statuses[el] for el in lines]
    line_colours = [colours.LINE_COLOURS.get(el) for el in lines]

    for n, (rgb, s) in enumerate(zip(line_colours, status)):
        operation = pixel_operation(s)
        operation(n, *rgb)

    blinkt.show()


def main():
    while True:
        illuminate()
        time.sleep(120)


if __name__ == '__main__':
    main()
