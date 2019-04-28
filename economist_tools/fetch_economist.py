import os
import re
import requests
import subprocess
import time

""" Download The Economist and send to kindle if new """

def fetch(existant_versions):
    print('Fetching calibre recipe from Github')
    url = ('https://raw.githubusercontent.com/kovidgoyal/calibre/master/' +
           'recipes/economist.recipe')
    resp = requests.get(url)

    with open('economist.recipe', 'w') as f:
        f.writelines(resp.text)

    print('Making mobi file')
    cmd = 'ebook-convert economist.recipe economist.mobi'
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                            universal_newlines=True)
    early_termination = False
    article_count = 0

    for line in iter(proc.stdout.readline, ''):
        print(line, end='', flush=True)
        if 'Article downloaded' in line:
            article_count += 1
        match = re.search(r'Got cover.*print-covers/(\d{8})', line)
        if match:
            date = match.groups()[0]
            if date in existant_versions:
                print('Got version {} again'.format(date))
                proc.terminate()
                early_termination = True
                break

    if article_count < 50:
        print('Insufficient articles downloaded. Failed fetch.')
        early_termination = True
        return

    proc.stdout.close()
    proc.wait()

    filename = 'economist.{}.mobi'.format(date)
    if not early_termination:
        print('Generated {}'.format(filename))
    return filename


def send_message(dated_filename):
    print('Emailing')
    subprocess.run(['./email.sh'])


def run():
    while True:
        existant_versions = [el.split('.')[1] for el in os.listdir()
                             if el.endswith('.mobi')]
        dated_filename = fetch(existant_versions)

        if not dated_filename or os.path.exists(dated_filename):
            # The links are still being updated
            # Wait and retry in a few minutes
            print('Retrying in 5 minutes')
            time.sleep(5 * 60)
        else:
            open(dated_filename, 'a').close()
            send_message(dated_filename)
            print('Done.')
            return dated_filename

        if time.localtime().tm_hour > 20:
            return


def main():
    run()


if __name__ == '__main__':
    main()
