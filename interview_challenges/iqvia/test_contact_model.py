import json
import pytest
from unittest import mock

from contact_model import Base, Contact, Email


def test_foreign_keys():
    c = Contact(
        username='anna',
        first_name='Anna',
        last_name='Zander')
    e1 = Email(
        address='anna@gmail.com',
        contact=c)
    e2 = Email(
        address='anna@hotmail.com',
        contact=c)

    assert c.to_dict() == {
        'username': 'anna', 
        'first_name': 'Anna',
        'last_name': 'Zander',
        'emails': ['anna@gmail.com', 'anna@hotmail.com']}
    assert e1.to_dict() == {
        'address': 'anna@gmail.com', 'contact': 'anna'}
