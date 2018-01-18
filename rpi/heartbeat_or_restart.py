import os
import requests
import sys


def main():
    # Unknown error raised when the wifi adapter dies - restart RPi to "fix"
    url = 'http://www.google.com'
    try:
        requests.packages.urllib3.disable_warnings()
        _ = requests.get(url)
        print('Successful ping')
    except:
        sys.stderr.write('Failure to connect to Google. Restarting.\n')
        os.system('sudo shutdown -r now')


if __name__ == '__main__':
    main()
