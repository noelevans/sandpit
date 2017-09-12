import datetime
import encodings.idna
import numpy as np
import requests
import time
import unicornhat


LINES = ['central',  'circle',
         'central',  'circle',
         'jubilee',  'metropolitan',
         'jubilee',  'metropolitan',
         'northern', 'piccadilly',    # victoria
         'northern', 'piccadilly',    # victoria
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
        'victoria':     (  0, 152, 212),
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


def tube_status():
    requests.packages.urllib3.disable_warnings()
    resp = requests.get('http://api.tfl.gov.uk/Line/Mode/tube/Status').json()

    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in resp}
    return {line: STATUSES.get(statuses[line], 'bad')
            for line in statuses.keys()
            if line in LINES}


def weather_status():
    url = ('https://api.darksky.net/forecast/' +
           '09eb3c861a010137bff29ba16b13d3e1/51.576301,-0.349967?' +
           'units=si&exclude=minutely')

    requests.packages.urllib3.disable_warnings()
    resp  = requests.get(url).json()
    today = datetime.date.today()
    start = datetime.datetime.min
    end   = datetime.datetime.combine(datetime.date.today(),
                                      datetime.datetime.max.time())
    probas = [el['precipProbability']
              for el in resp['hourly']['data']
              if start < datetime.datetime.fromtimestamp(el['time']) < end]
    return max(probas or 0)


def update_hat(tube):
    unicornhat.set_layout(unicornhat.AUTO)
    unicornhat.rotation(180)
    unicornhat.brightness(0.5)
    width, height = unicornhat.get_shape()

    ws = weather_status()
    weather = np.zeros(16).astype(int)
    weather[:int(round(16 * ws))] = 1
    w2 = np.hstack(weather.reshape(8, 2).T)
    weather = np.vstack([w2, w2, w2]).T * 255
    status = np.concatenate([tube, weather])
    pixel_statuses = status.reshape(width, height, 3)

    for h in range(height):
        for w in range(width):
            unicornhat.set_pixel(h, w, *pixel_statuses[w, h])
    unicornhat.show()


def main():
    status = layout(tube_status())
    update_hat(status)
    time.sleep(50)


if __name__ == '__main__':
    main()
