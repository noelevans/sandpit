from celery import Celery
from random import randint
import requests


app = Celery(
    'auto_generation_worker', 
    backend='redis://localhost', 
    broker='redis://localhost')


def random_name():
    letters = [chr(randint(0, 25) + ord('a')) for _ in range(randint(6, 16))]
    return ''.join(letters)


@app.task
def make_random_contact():
    first_name = random_name()
    last_name = random_name()
    username = ''.join([first_name, last_name])

    json_data = {
        'email': [
            '{}@gmail.com'.format(username), 
            '{}@hotmail.com'.format(username)],
        'first_name': first_name,
        'last_name': last_name
    }
    requests.post(
        'http://localhost:5000/api/create/user:{}'.format(username),
        json=json_data)
    return username


@app.task
def remove_old_contact(username):
    if username:
        requests.delete(
            'http://localhost:5000/api/delete/user:{}'.format(username))
