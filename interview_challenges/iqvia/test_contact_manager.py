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

    def check_anna(resp_data):
        assert resp_data['email'] == ['email:anna@gmail.com', 'email:az@email.com']
        assert resp_data['first_name'] == 'Anna'
        assert resp_data['last_name'] == 'Zander'

    get_data = {
        'user:anna': json.dumps({
            'first_name': 'Anna',
            'last_name': 'Zander'}),    
        'email:anna@gmail.com': 'anna', 
        'email:az@email.com': 'anna'}
    scan_idx = {
        'user:*': ['user:anna'], 
        'email:*': ['email:anna@gmail.com', 'email:az@email.com']}

    with mock.patch('redis.StrictRedis.get', lambda _, key: get_data.get(key)):
        with mock.patch('redis.StrictRedis.scan_iter', lambda _, key: scan_idx[key]):

            check_anna(json.loads(client.get('/api/get/email:az@email.com').data))
            check_anna(json.loads(client.get('/api/get/email:anna@gmail.com').data))

            check_anna(json.loads(client.get('/api/get/user:anna').data))
            
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
            assert client.get('/api/get_all/user').json == {
                'user:anna': {'email': ['anna@gmail.com', 'az@email.com'], 
                              'first_name': 'Anna', 'last_name': 'Zander'}, 
                'user:clare': {'email': ['clare@outlook.com', 'ccuthbert@hotmail.com'], 
                               'first_name': 'Clare', 'last_name': 'Cuthbert'}}

    emails = {'email:az@email.com': 'anna',
              'email:anna@gmail.com': 'anna'}
    mock_keys = ['email:az@email.com', 'email:anna@gmail.com']
    with mock.patch('redis.StrictRedis.get', lambda _, key: emails[key]):
        with mock.patch('redis.StrictRedis.scan_iter',
                        return_value=mock_keys):
            assert client.get('/api/get_all/email').json == {
                'email:anna@gmail.com': 'anna', 
                'email:az@email.com': 'anna'}


def test_create(client):
    with mock.patch('redis.StrictRedis.set') as mock_set:
        client.post('/api/contact/user:anna', data=data['user:anna'])
        assert mock_set.called_with('user:anna', data['user:anna'])
        assert mock_set.called_with('email:anna@gmail.com', 'anna')
        assert mock_set.called_with('email:az@email.com', 'anna')


def test_delete_contact(client):
    fake_redis = {'user:anna': 1, 'email:anna@hotmail.com': 1}
    mock_delete = lambda _, keys: fake_redis.get(keys[0], 0)

    with mock.patch('redis.StrictRedis.delete', mock_delete):
        assert client.delete('/api/delete/user:anna').status_code == 200
        assert client.delete('/api/delete/user:barry').status_code == 409
        assert client.delete('/api/delete/email:anna@hotmail.com').status_code == 200
        assert client.delete('/api/delete/email:barry@hotmail.com').status_code == 409


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
            assert mock_set.called_with(
                'email:anna@hotmail.com', 'anna')


def main():
    pytest.main()


if __name__ == '__main__':
    main()
