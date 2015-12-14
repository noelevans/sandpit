import requests
from piglow import PiGlow


def update():
    requests.packages.urllib3.disable_warnings()
    resp = requests.get('http://api.tfl.gov.uk/Line/Mode/tube/Status').json()

    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in resp}
    return {k: statuses[k] == 'Good Service' for k in statuses.keys()}


def main():
    piglow = PiGlow()
    piglow.all(0)
    running = update()
    important_lines_running = True

    if running.pop('metropolitan'):
        piglow.led1(1)
    else:
        piglow.arm1(1)
        important_lines_running = False

    if running.pop('jubilee'):
        piglow.led7(1)
        piglow.led8(1)
    else:
        piglow.arm2(1)
        important_lines_running = False

    # Waterloo and City line never runs on the weekend
    if datetime.date.today().isoweekday() in (6, 7):
        running.pop('waterloo-city')

    if all(running.values()):
        piglow.led13(1)
        piglow.led14(1)
        piglow.led15(1)
    else:
        piglow.arm3(1)
        if important_lines_running:
            # asthetic tweak to avoid bright white LED always being on "alone"
            piglow.led18(0)


if __name__ == '__main__':
    main()
