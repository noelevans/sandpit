import datetime
import os
import requests


def update():
    requests.packages.urllib3.disable_warnings()
    resp = requests.get('http://api.tfl.gov.uk/Line/Mode/tube/Status').json()

    return {el['id']: el['lineStatuses'][0]['statusSeverityDescription'] for el in resp}


def email(lines):
    with open('curl_raw_command.sh') as f:
        raw_command = f.read()

    if lines:
        subject = 'Tube delays for commute'
        body = ', '.join(': '.join([line.capitalize(), s]) for line, s in lines.items())
    else:
        subject = 'Good service for commute'
        body = 'Good service on all lines'

    # We must have this running on PythonAnywhere - Monday to Sunday.
    # Ignore Saturday and Sunday
    if datetime.date.today().isoweekday() in range(1, 6):
        os.system(raw_command.format(subject=subject, body=body))


def main():
    commute_lines = ['metropolitan', 'jubilee', 'central']
    status = update()
    delays = {c: status[c] for c in commute_lines if status[c] != 'Good Service'}
    email(delays)


if __name__ == '__main__':
    main()
