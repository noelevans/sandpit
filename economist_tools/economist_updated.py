import datetime
import requests
import time

import emailing
import fetch_economist


def alert(body):
    return emailing.send(subject='New Economist', body=body)


def main():
    soft_link = 'https://www.economist.com/printedition'
    # The URL forwards to a datestamped URL for this week
    original_fwd = requests.get(soft_link).url
    original_date = original_fwd.split('/')[-1]

    while True:
        current_fwd = requests.get(soft_link).url
        current_date = current_fwd.split('/')[-1]

        print(current_fwd, original_fwd)
        print(current_date, original_date)

        if current_date > original_date:
            alert('A new Economist has been released: ' + current_date)
            result = fetch_economist.run()
            if result:
                alert('Sent to kindle: {}'.format(result))
            return

        if datetime.datetime.now().hour > 19:
            return

        is_thursday = datetime.datetime.today().isoweekday() == 4
        if is_thursday and datetime.datetime.now().hour > 15:
            minutes = 5
        else:
            minutes = 30
        time.sleep(60 * minutes)



if __name__ == '__main__':
    main()