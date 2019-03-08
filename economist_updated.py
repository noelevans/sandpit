import datetime
import requests
import time

import emailing


def alert(body):
    emailing.send(subject='New Economist', body=body)


def main():
    soft_link = 'https://www.economist.com/printedition'
    # The URL forwards to a datestamped URL for this week
    original_fwd = requests.get(soft_link).url
    original_date = original_fwd.split('/')[-1]

    while True:
        is_thursday = datetime.date.today().isoweekday() == 4
        if is_thursday and datetime.datetime.now().hour > 14:
            minutes = 5
        else:
            minutes = 30
        time.sleep(60 * minutes)

        current_fwd = requests.get(soft_link).url
        current_date = current_fwd.split('/')[-1]

        if current_date > original_date:
            alert('A new Economist has been released: ' + current_date)
            return

        if datetime.datetime.now().hour > 19:
            return


if __name__ == '__main__':
    main()
