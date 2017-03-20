import datetime
import json
import os
import urllib2


def update():
    url = 'http://api.tfl.gov.uk/Line/Mode/tube/Status'
    resp = json.loads(urllib2.urlopen(url).read())

    return {el['id']: el['lineStatuses'][0]['statusSeverityDescription'] for el in resp}


def email(lines):
    with open('curl_raw_command.sh') as f:
        raw_command = f.read()

    if lines:
        subject = 'Tube delays for commute'
        body = ', '.join(': '.join([line.capitalize(), s]) for line, s in status.items())
    else:
        subject = 'Good service for commute'
        body = 'Good service on all lines'

    os.system(raw_command.format(subject=subject, body=body))


def main():
    commute_lines = ['metropolitan', 'jubilee', 'central']
    status = update()
    delays = {c: status[c] for c in commute_lines if status[c] != 'Good Service'}
    email(delays)


if __name__ == '__main__':
    main()
