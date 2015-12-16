import requests
from piglow import PiGlow


STATUSES = {'Good Service': 'GOOD',
            'Minor Delays': 'OK'}   # All other statuses are bad

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
        running = update()
    except:     # Unknown error raised when the wifi adapter dies
        piglow.orange(1)

    important_lines_running = True

    # {'GOOD': [1],
    #  'OK': [1, 2]}.get(running['metropolitan'], [1, 2, 3, 4, 5, 6])
    if running['metropolitan'] == 'GOOD':
        piglow.led(1, 1)
    elif running['metropolitan'] == 'OK':
            piglow.led(1, 1)
            piglow.led(2, 1)
    else:
        [piglow.led(n, 1) for n in [1, 2, 3, 4, 5, 6]]
        important_lines_running = False
    running.pop('metropolitan')

    if running['jubilee'] == 'GOOD':
        piglow.led(7, 1)
        piglow.led(8, 1)
    elif running['jubilee'] == 'OK':
        piglow.led(7, 1)
        piglow.led(8, 1)
        piglow.led(9, 1)
    else:
        [piglow.led(n, 1) for n in [7, 8, 9, 10, 11, 12]]
        important_lines_running = False
    running.pop('jubilee')

    # Waterloo and City line never runs on the weekend
    if datetime.date.today().isoweekday() in (6, 7):
        running.pop('waterloo-city')

    if all('GOOD' == v for v in running.values()):
        piglow.led(13, 1)
        piglow.led(14, 1)
        piglow.led(15, 1)
    elif all(v in ('GOOD', 'OK') for v in running.values()):
        piglow.led(13, 1)
        piglow.led(14, 1)
        piglow.led(15, 1)
        piglow.led(16, 1)
    else:
        [piglow.led(n, 1) for n in [13, 14, 15, 16, 17, 18]]
        if important_lines_running:
            # asthetic tweak to avoid bright white LED always being on "alone"
            piglow.led(18, 0)


if __name__ == '__main__':
    main()
