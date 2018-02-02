"""
Read in files transport_lines.txt.

Handle these cases carefully:

    More or less than 8 lines

"""

import colours


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


def illuminate():
    lines = line_choices()
    status = transport_status()
    line_colours = [colours.LINE_COLOURS.get(el) for el in lines]

    # for n in range(8):
    #     blinkt.set_pixel(x, r, g, b, brightness=None)


if __name__ == '__main__':
    main()
