import json
import requests
import time

from PyGlow import PyGlow


URL = 'https://api.tfl.gov.uk/Line/Mode/tube/Status'

def update():
    resp = requests.get(URL)
    ol = resp.json()

    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in ol}
    return {k: statuses[k] == 'Good Service' for k in statuses.keys()}


def main():
    pyglow = PyGlow()
    good = {brightness:  85, speed=None, pulse=False}
    bad  = {brightness: 170, speed=1000, pulse=True}

    while True:
        good_statuses = update()

        led_settings = lambda test: test and good or bad
        met_args = led_settings(good_statuses['metropolitan'])
        jub_args = led_settings(good_statuses['jubilee'])
        all_args = led_settings(all(good_statuses.values())

        pyglow.arm(1, **met_args)
        pyglow.arm(2, **jub_args)
        pyglow.arm(3, **all_args)

        time.sleep(30)


if __name__ == '__main__':
    main()

