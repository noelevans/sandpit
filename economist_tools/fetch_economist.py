import os
import re
import requests
import subprocess
import time

""" Download The Economist and send to kindle if new """

def fetch(existant_versions):
    # print('Fetching calibre recipe from Github')
    # url = ('https://raw.githubusercontent.com/kovidgoyal/calibre/master/' +
    #        'recipes/economist.recipe')
    # resp = requests.get(url)

    # with open('economist.recipe', 'w') as f:
    #     f.writelines(resp.text)

    print('Making mobi file')
    cmd = 'ebook-convert economist.recipe economist.mobi'
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                            universal_newlines=True)
    early_termination = False
    for line in iter(proc.stdout.readline, ''):
        print(line, end='', flush=True)
        match = re.search(r'Got cover.*print-covers/(\d{8})', line)
        if match:
            date = match.groups()[0]
            if date in existant_versions:
                print('Got version {} again'.format(date))
                proc.terminate()
                early_termination = True
                break

    proc.stdout.close()
    proc.wait()

    filename = 'economist.{}.mobi'.format(date)
    if not early_termination:
        print('Generated {}'.format(filename))
    return filename


def send_message(dated_filename):
    '''
    mail -A ~/repo/sandbox/economist_tools/economist.mobi -s "Email File 3: mail" -a "From: noelevans@gmx.co.uk" noelevans@gmail.com < /dev/null
    '''
    print('Emailing')
    subprocess.run(['./email.sh', dated_filename])


def run():
    while True:
        existant_versions = [el.split('.')[1] for el in os.listdir()
                             if el.endswith('.mobi')]
        dated_filename = fetch(existant_versions)

        if os.path.exists(dated_filename):
            # The links are still being updated
            # Wait and retry in a few minutes
            print('Retrying in 5 minutes')
            time.sleep(5 * 60)
        else:
            open(dated_filename, 'a').close()
            send_message(dated_filename)
            print('Done.')
            return dated_filename

        if time.localtime().tm_hour > 22:
            return


def main():
    run()


if __name__ == '__main__':
    main()
