import datetime
import os
import re
import requests
import socket
import time

import emailing
import fetch_economist


def alert(body):
    return emailing.send(subject='New Economist', body=body)


def main():
    # The URL forwards to a datestamped URL for this week
    soft_link = 'https://www.economist.com/printedition'

    working_dir = os.path.dirname(os.path.realpath(__file__))
    previous_editions = [
        el.split('.')[1]
        for el in os.listdir(working_dir) 
        if re.match('economist.\d{8}.mobi', el)
    ]

    while True:
        current_fwd = requests.get(soft_link).url
        current_date = current_fwd.split('/')[-1]

        if current_date not in previous_editions:
            alert('A new Economist has been released: {}. ({})'.format(
                    current_date,
                    socket.gethostname(),
                )
            )
            result = fetch_economist.run()
            if result:
                alert('Sent to kindle: {}'.format(result))
            return

        hour = datetime.datetime.now().hour
        if hour > 20 or hour < 6:
            print('Night hours. Exiting.')
            return

        is_thursday = datetime.datetime.today().isoweekday() == 4
        if is_thursday and hour > 15:
            minutes = 5
        elif is_thursday and hour > 14:
            minutes = 20
        elif is_thursday:
            minutes = 40
        else:
            minutes = 240
        print('Sleeping for {} minutes'.format(minutes))
        time.sleep(60 * minutes)

        print('')


if __name__ == '__main__':
    main()
