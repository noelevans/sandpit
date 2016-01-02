import datetime
import os
import requests
from piglow import PiGlow


STATUSES = {'Good Service': 'GOOD',
            'Minor Delays': 'OK'}   # All other statuses are 'BAD'

def update():
    requests.packages.urllib3.disable_warnings()
    resp = requests.get('http://api.tfl.gov.uk/Line/Mode/tube/Status').json()

    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in resp}
    return {k: STATUSES.get(statuses[k], 'BAD') for k in statuses.keys()}


def main():
    piglow = PiGlow()
    piglow.all(0)
    try:
        status = update()
    except:     # Unknown error raised when the wifi adapter dies
        piglow.blue(1)
        os.system('sudo shutdown -r now')

    met_status = status.pop('metropolitan')
    jubilee_status = status.pop('jubilee')

    if datetime.date.today().isoweekday() in (6, 7):
        # No Waterloo and City service on the weekend
        status.pop('waterloo-city')

    # Reminder: sets can't be keys to dicts but frozensets can
    other_statuses = frozenset(status.values())
    other_status = {frozenset(['GOOD']): 'GOOD',
                    frozenset(['GOOD', 'OK']): 'OK'}.get(other_statuses, 'BAD')

    met_leds = {'GOOD': [1],
                'OK':   [1, 2],
                'BAD':  [1, 2, 3, 4, 5, 6]}[met_status]

    jubilee_leds = {'GOOD': [7],
                    'OK':   [7, 8],
                    'BAD':  [7, 8, 9, 10, 11, 12]}[jubilee_status]

    other_leds = {'GOOD': [13],
                  'OK':   [13, 14],
                  'BAD':  [13, 14, 15, 16, 17, 18]}[other_status]

    [piglow.led(n, 1) for n in met_leds + jubilee_leds + other_leds]


if __name__ == '__main__':
    main()
