"""
Read in files transport_lines.txt.

Handle these cases carefully:

    More or less than 8 lines

"""

import blinkt
import colours
import multiprocessing
import requests
import time


REFRESH_TIME = 5 * 60


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

    def good_op(x, rgb):
        start = time.time()
        while time.time() < start + REFRESH_TIME:
            blinkt.set_pixel(x, *rgb, brightness=0.04)
            blinkt.show()
            time.sleep(1)

    def flash_op(x, rgb):
        start = time.time()
        while time.time() < start + REFRESH_TIME:
            blinkt.set_pixel(x, *rgb, brightness=0.04)
            blinkt.show()
            time.sleep(1.5)
            blinkt.set_pixel(x, *rgb, brightness=0.0)
            blinkt.show()
            time.sleep(1.5)

    def off_op(x, rgb):
        start = time.time()
        while time.time() < start + REFRESH_TIME:
            blinkt.set_pixel(x, *rgb, brightness=0)
            blinkt.show()
            time.sleep(1)

    return {
            'GOOD': good_op,
            'OK':   flash_op,
            'BAD':  off_op,
        }[status]


def illuminate():
    lines = line_choices()
    all_statuses = transport_status()
    status = [all_statuses[el] for el in lines]
    line_colours = [colours.LINE_COLOURS.get(el) for el in lines]

    processes = []
    for n, (rgb, s) in enumerate(zip(line_colours, status)):
        print(s)
        operation = pixel_operation(s)
        process = multiprocessing.Process(target=operation, args=(n, rgb))
        process.start()
        processes.append(process)

    for p in processes:
        p.join()
    print('All processes joined')

def main():
    while True:
        illuminate()


if __name__ == '__main__':
    main()
