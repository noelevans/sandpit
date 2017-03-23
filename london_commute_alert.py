import datetime
import os
import requests


def update():
    url = 'http://api.tfl.gov.uk/Line/Mode/tube/Status'
    resp = requests.get(url).json()
    result = {}

    for el in resp:
        value = el['lineStatuses'][0]
        if value['statusSeverityDescription'] != 'Good Service':
            message = '{} ({})'.format(value['statusSeverityDescription'],
                                       value['reason'])
            result[el['id']] = message

    return result


def email(lines):
    with open('curl_raw_command.sh') as f:
        raw_command = f.read()

    subject = 'Tube delays for commute'
    body = '\n\n'.join(': '.join([line.capitalize(), s]) for line, s in lines.items())

    # We must have this running on PythonAnywhere - Monday to Sunday.
    # Ignore Saturday and Sunday
    if datetime.date.today().isoweekday() in range(1, 6):
        os.system(raw_command.format(subject=subject, body=body))


def main():
    commute_lines = ['metropolitan', 'jubilee', 'central']
    status = update()
    print(status)
    delays = {c: status[c] for c in commute_lines if status.get(c)}

    if delays:
        email(delays)


if __name__ == '__main__':
    main()
