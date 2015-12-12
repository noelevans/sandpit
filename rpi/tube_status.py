import requests
from piglow import PiGlow


URL = 'http://api.tfl.gov.uk/Line/Mode/tube/Status'
requests.packages.urllib3.disable_warnings()


def update():
    resp = requests.get(URL)
    ol = resp.json()

    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in ol}
    return {k: statuses[k] == 'Good Service' for k in statuses.keys()}


def main():
    piglow = PiGlow()
    piglow.all(0)
    running = update()

    if running['metropolitan']:
        piglow.led1(1)
    else:
        piglow.arm1(1)

    if running['jubilee']:
        piglow.led7(1)
        piglow.led8(1)
    else:
        piglow.arm2(1)

    if all(running.values()):
        piglow.led13(1)
        piglow.led14(1)
        piglow.led15(1)
    else:
        piglow.arm3(1)


if __name__ == '__main__':
    main()
