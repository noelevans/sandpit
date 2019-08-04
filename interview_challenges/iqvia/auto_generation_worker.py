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
    email1 = '{}@gmail.com'.format(username)
    email2 = '{}@hotmail.com'.format(username)

    json_data = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name
    }
    requests.post(
        'http://localhost:5000/api/create/contact',
        json=json_data)
    requests.post(
        'http://localhost:5000/api/create/email',
        json={'username': username, 'address':email1})
    requests.post(
        'http://localhost:5000/api/create/email',
        json={'username': username, 'address':email2})
    return {'username': username, 'email1': email1, 'email2': email2}


@app.task
def remove_old_contact(deletions):
    if deletions:
        requests.delete(
            'http://localhost:5000/api/delete/email/{}'.format(
                deletions['email1']))
        requests.delete(
            'http://localhost:5000/api/delete/email/{}'.format(
                deletions['email2']))
        requests.delete(
            'http://localhost:5000/api/delete/contact/{}'.format(
                deletions['username']))
