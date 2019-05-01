import os
import sys


def send(subject, body):
    os.chdir(sys.path[0])
    with open('curl_raw_command.sh') as f:
        raw_command = f.read()
        os.system(raw_command.format(subject=subject, body=body))
