import time

from auto_generation_worker import make_random_contact, remove_old_contact


def make_contact():
    result = make_random_contact.delay()
    time.sleep(15)
    return result.get()


cleanups = [None, None, None]

while True:
    cleanups.append(make_contact())
    remove_old_contact.delay(cleanups.pop(0))
