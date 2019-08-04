import json
import pytest
from unittest import mock

import contact_manager
from contact_model import Base, Contact, Email


CONTACTS = {
    'anna': Contact(
        username='anna', 
        first_name='Anna', 
        last_name='Zander'),
    'clare': Contact(
        username='clare',
        first_name='Clare',
        last_name='Cuthburt')}


@pytest.fixture
def client():
    contact_manager.app.config['TESTING'] = True
    return contact_manager.app.test_client()


def test_get(client):
    with mock.patch('contact_manager.session') as sm:
        sm.query.return_value = {'anna': Contact(
            username='anna', 
            first_name='Anna', 
            last_name='Zander')}

        assert client.get('/api/get/contact/barry').status_code == 404
        assert client.get('/api/get/contact/anna').status_code == 200

        resp_data = client.get('/api/get/contact/anna').get_json()
        assert resp_data['first_name'] == 'Anna'
        assert resp_data['last_name'] == 'Zander'


def test_get_all(client):
    with mock.patch('contact_manager.session') as sm:
        sm.query.return_value.all.return_value = CONTACTS.values()
        resp = client.get('/api/get/contacts').get_json()
        assert resp[0]['username'] == 'anna'
        assert resp[1]['username'] == 'clare'


def test_create(client):
    with mock.patch('contact_manager.session') as sm:
        client.post(
            '/api/create/contact', 
            data=json.dumps({
                'username': 'anna', 
                'first_name': 'Anna', 
                'last_name': 'Zander'}))
        assert sm.add.called_with(CONTACTS['anna'])

        client.post(
            '/api/create/email', 
            data=json.dumps({
                'username': 'anna', 
                'address': 'anna@hotmail.com'}))
        assert sm.add.called_with(CONTACTS['anna'])


def test_delete_contact(client):
    with mock.patch('contact_manager.session') as sm:
        sm.query.return_value = CONTACTS
        assert client.delete('/api/delete/email/barry@gmail.com').status_code == 400
        assert client.delete('/api/delete/contact/anna').status_code == 200
        assert sm.delete.called_with(CONTACTS['anna'])


def test_update_contact(client):
    with mock.patch('contact_manager.session') as sm:
        sm.query.return_value = CONTACTS
        resp_data = client.put(
            '/api/update/contact/anna',
            json={'last_name': 'Bander'}).get_json()
        print(resp_data)
        assert resp_data['last_name'] == 'Bander'
