import datetime
import os
import requests


def update(lines):
    url = 'http://api.tfl.gov.uk/Line/Mode/tube/Status'
    resp = requests.get(url).json()
    result = []

    for el in resp:
        value = el['lineStatuses'][0]
        state = value['statusSeverityDescription']
        if el['id'] in lines and state != 'Good Service':
            result.append('{}: {} ({})'.format(
                el['id'].capitalize(),
                value['statusSeverityDescription'],
                value['reason']))

    return result


def email(lines):
    with open('curl_raw_command.sh') as f:
        raw_command = f.read()

    # We must have this running on PythonAnywhere - Monday to Sunday.
    # Ignore Saturday and Sunday
    if datetime.date.today().isoweekday() in range(1, 6):
        os.system(raw_command.format(subject='Tube delays for commute', 
                                     body='\n\n'.join(lines)))


def main():
    commute_lines = ['metropolitan', 'jubilee', 'central']
    delays = update(commute_lines)
    if delays:
        email(delays)


if __name__ == '__main__':
    main()
