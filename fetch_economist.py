import os
import re
import time
import subprocess

""" Download The Economist and send to kindle if new """

def fetch():
    url = ('https://raw.githubusercontent.com/kovidgoyal/calibre/master/' +
           'recipes/economist.recipe')
    cmd_1 = ['curl', url, '>', 'economist.recipe']
    subprocess.run(cmd_1, check=True)

    cmd_2 = ['ebook-convert', 'economist.recipe', 'economist.mobi']
    output = subprocess.run(cmd_2, stdout=subprocess.PIPE, check=True)

    for line in output:
        match = re.search(r'Got cover.*/(\d{8})', s)
        if match:
            date = match.group()
            break

    return 'economist.{}.mobi'.format(date)


def main():
    while True:
        dated_filename = fetch()

        if os.path.exists(dated_filename):
            # The links are still being updated
            # Wait and retry in a few minutes
            time.sleep(5 * 60)
        else:
            open(dated_filename, 'a').close()
            subprocess.run([
                'calibre-smtp', '-a', 'economist.mobi',
                '-u', 'SENDERNAME@PROVIDER.com',
                '-p', 'PASSWORD',
                '-r', 'smtp.PROVIDER.com',
                '--port', '587',
                'SENDERNAME@PROVIDER.com',
                'USERNAME@free.kindle.com'])
            return

        if time.localtime().tm_hour > 22:
            return


if __name__ == '__main__':
    main()
