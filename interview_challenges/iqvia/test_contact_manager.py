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


def test_get_contact():
    mock_get = lambda _, username: data.get(username)

    with mock.patch('redis.StrictRedis.get', mock_get):
        resp_data = client.get('/api/contact/anna').get_json()
        assert 'anna' == resp_data['username']
        assert 'anna@gmail.com' == resp_data['email']
        assert 'Anna' == resp_data['first_name']
        assert 'Zander' == resp_data['last_name']

        assert client.get('/api/contact/barry') is 7


def test_get_all_contacts():
    all_contacts = [data, {'clare': json.dumps({
        'username': 'clare',
        'email': 'clare@outlook.com',
        'first_name': 'Clare',
        'last_name': 'Cuthbert'
    })}]
    assert 2 == len(client.get('/api/contacts'))


@mock.patch('redis.StrictRedis.set')
def test_create_contact(mock_set):
    client.post('/api/contact', data=data)
    assert mock_set.called_with('anna', data)


def test_delete_contact():
    expected_usernames = [['anna'], ['barry']]

    def mock_delete(_, usernames):
        if usernames == expected_usernames[0]:
            expected_usernames.pop(0)
        return {'anna': 1}.get(usernames[0], 0)

    with mock.patch('redis.StrictRedis.delete', mock_delete):
        assert 1 == contact_manager.delete_contact('anna')

        with pytest.raises(Exception):
            contact_manager.delete_contact('barry')

@mock.patch('redis.StrictRedis.set')
def test_update_contact(mock_set):
    mock_get = lambda _, username: data.get(username)

    with mock.patch('redis.StrictRedis.get', mock_get):
        contact_manager.update_contact(
                'anna', json.dumps({
                'last_name': 'Bander', 'email': 'anna@hotmail.com'}))
        
        assert mock_set.called_with(
                'anna',
                json.dumps({
                    'username': 'anna',
                    'email': 'anna@hotmail.com',
                    'first_name': 'Anna',
                    'last_name': 'Bander'
                }))


@mock.patch('redis.StrictRedis.delete')
@mock.patch('redis.StrictRedis.set')
@mock.patch('redis.StrictRedis.get', return_value=['anna'])
def test_update_contact_change_username(mock_delete, mock_set, mock_get):
    contact_manager.update_contact('anna', json.dumps({
        'username': 'annab',
        'last_name': 'Bander'}))

    assert mock_delete.called_with(['anna'])
    assert mock_set.called_with('annab', json.dumps({
        'username': 'annab',
        'email': 'anna@gmail.com',
        'first_name': 'Anna',
        'last_name': 'Bander'
    }))
    

def main():
    pytest.main()


if __name__ == '__main__':
    main()

