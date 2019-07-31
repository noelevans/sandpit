import json
import pytest
from unittest import mock

import contact_manager


data = {'user:anna': json.dumps({
    'email': ['anna@gmail.com', 'az@email.com'],
    'first_name': 'Anna',
    'last_name': 'Zander'
})}

@pytest.fixture
def client():
    contact_manager.app.config['TESTING'] = True
    return contact_manager.app.test_client()


def test_get(client):
    mock_get = lambda _, key: data.get(key)

    with mock.patch('redis.StrictRedis.get', mock_get):
        resp_data = json.loads(client.get('/api/get/user:anna').data)
        assert resp_data['email'] == ['anna@gmail.com', 'az@email.com']
        assert resp_data['first_name'] == 'Anna'
        assert resp_data['last_name'] == 'Zander'

        assert client.get('/api/get/user:barry').status_code == 404


def test_get_all(client):
    all_contacts = data.copy()
    all_contacts.update({'user:clare': json.dumps({
        'email': ['clare@outlook.com', 'ccuthbert@hotmail.com'],
        'first_name': 'Clare',
        'last_name': 'Cuthbert'
    })})
    mock_get = lambda _, key: all_contacts[key]
    with mock.patch('redis.StrictRedis.get', mock_get):
        with mock.patch('redis.StrictRedis.scan_iter',
                return_value=['user:anna', 'user:clare']):
            assert len(client.get('/api/get_all/user').json) == 2


def test_create(client):
    with mock.patch('redis.StrictRedis.set') as mock_set:
        client.post('/api/contact/user:anna', data=data['user:anna'])
        assert mock_set.called_with('user:anna', data['user:anna'])


def test_delete_contact(client):
    mock_delete = lambda _, keys: {'user:anna': 1}.get(keys[0], 0)

    with mock.patch('redis.StrictRedis.delete', mock_delete):
        assert client.delete('/api/delete/user:anna').status_code == 200
        assert client.delete('/api/delete/user:barry').status_code == 409


def test_update_contact(client):
    with mock.patch('redis.StrictRedis.set') as mock_set:
        mock_get = lambda _, key: data.get(key)

        with mock.patch('redis.StrictRedis.get', mock_get):
            client.put(
                '/api/update/user:anna',
                json=({
                    'last_name': 'Bander',
                    'email': ['anna@hotmail.com']}))

            assert mock_set.called_with(
                'user:anna',
                json.dumps({
                    'email': 'anna@hotmail.com',
                    'first_name': 'Anna',
                    'last_name': 'Bander'
                    }))


def main():
    pytest.main()


if __name__ == '__main__':
    main()
