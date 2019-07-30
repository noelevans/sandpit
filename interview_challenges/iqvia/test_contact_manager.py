import json
import pytest
from unittest import mock

import contact_manager


data = {'anna': json.dumps({
    'username': 'anna',
    'email': 'anna@gmail.com',
    'first_name': 'Anna',
    'last_name': 'Zander'
})}

@pytest.fixture
def client():
    contact_manager.app.config['TESTING'] = True
    return contact_manager.app.test_client()


def test_get_contact(client):
    mock_get = lambda _, username: data.get(username)

    with mock.patch('redis.StrictRedis.get', mock_get):
        resp_data = json.loads(client.get('/api/contact/anna').data)
        assert resp_data['username'] == 'anna'
        assert resp_data['email'] == 'anna@gmail.com'
        assert resp_data['first_name'] == 'Anna'
        assert resp_data['last_name'] == 'Zander'

        assert client.get('/api/contact/barry').status_code == 404


def test_get_all_contacts(client):
    all_contacts = [data, {'clare': json.dumps({
        'username': 'clare',
        'email': 'clare@outlook.com',
        'first_name': 'Clare',
        'last_name': 'Cuthbert'
    })}]
    mock_get = lambda _, username: all_contacts
    with mock.patch('redis.StrictRedis.get', mock_get):
        with mock.patch('redis.StrictRedis.scan_iter',
                        return_value=['anna', 'clare']):
            assert len(client.get('/api/contacts').json) == 2


def test_create_contact(client):
    with mock.patch('redis.StrictRedis.set') as mock_set:
        client.post('/api/contact', data=data)
        assert mock_set.called_with('anna', data)


def test_delete_contact(client):
    mock_delete = lambda _, usernames: {'anna': 1}.get(usernames[0], 0)

    with mock.patch('redis.StrictRedis.delete', mock_delete):
        print(dir(client))
        assert client.delete('/api/contact/delete/anna').status_code == 200
        assert client.delete('/api/contact/delete/barry').status_code == 409


def test_update_contact(client):
    with mock.patch('redis.StrictRedis.set') as mock_set:
        mock_get = lambda _, username: data.get(username)

        with mock.patch('redis.StrictRedis.get', mock_get):
            client.put(
                '/api/contact/update',
                json=({
                    'last_name': 'Bander',
                    'email': 'anna@hotmail.com'}))

            assert mock_set.called_with(
                'anna',
                json.dumps({
                    'username': 'anna',
                    'email': 'anna@hotmail.com',
                    'first_name': 'Anna',
                    'last_name': 'Bander'
                    }))


def main():
    pytest.main()


if __name__ == '__main__':
    main()
