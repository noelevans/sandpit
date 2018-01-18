import datetime
import os
import requests
import sys


def update(lines):
    url = 'http://api.tfl.gov.uk/Line/Mode/tube/Status'
    resp = requests.get(url).json()
    result = []

    for el in resp:
        value = el['lineStatuses'][0]
        state = value['statusSeverityDescription']
        if el['id'] in lines and state != 'Good Service':
            result.append('{}: {} ({})'.format(
                el['id'].capitalize(), state, value['reason']))

    return result


def email(delays):
    os.chdir(sys.path[0])
    with open('curl_raw_command.sh') as f:
        raw_command = f.read()

    # Running on PythonAnywhere - Monday to Sunday. Skip on the weekend
    if delays and datetime.date.today().isoweekday() in range(1, 6):
        os.system(raw_command.format(subject='Tube delays for commute',
                                     body='\n\n'.join(delays)))


def main():
    commute_lines = ['metropolitan', 'jubilee', 'central']
    email(update(commute_lines))


if __name__ == '__main__':
    main()
