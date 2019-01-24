import flask
import json
import pytest
import sqlite3
from   unittest import mock

import app


def test_fill_db():
    cursor = app.fill_db(open('positions.csv'))
    assert cursor is not None

    expected = [
        ("Mathilde Maersk", 9632179),
        ("Australian Spirit", 9247455),
        ("MSC Preziosa", 9595321)]
    for row, ex in zip(cursor.execute('select * from Ships'), expected):
        assert row == ex

    expected = {
        0:      (9632179,'2019-01-15 09:44:27+00',
                    51.8737335205078,2.73133325576782),
        1999:   (9247455,'2019-01-02 22:16:13+00',
                    1.24526834487915,103.916152954102)
    }
    for n, row in enumerate(cursor.execute('select * from Positions')):
        if n in expected:
            assert row == expected.get(n)

    assert n == 1999


def simple_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    c.execute('''create table Ships (name text, imo integer)''')
    c.execute('''create table Positions (
                    imo integer,
                    timestamp text,
                    latitude real,
                    longitude real)''')
    c.execute('insert into Ships values ("Mathilde Maersk", 9632179)')

    # Include out of order positions to ensure timestamp sorting
    c.execute('insert into Positions values (%s, "%s", %s, %s)' %
        (9632179,'2018',51.8,2.7))
    c.execute('insert into Positions values (%s, "%s", %s, %s)' %
        (9632179,'2019',51.8,2.7))
    c.execute('insert into Positions values (%s, "%s", %s, %s)' %
        (9632179,'2017',51.8,2.7))

    conn.commit()
    return c


@mock.patch('app.get_db')
def test_ships(mock_get_db):
    cursor = simple_db()
    mock_get_db.return_value = cursor
    response = app.app.test_client().get('/api/ships/')
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data == [{'imo': '9632179', 'name': 'Mathilde Maersk'}]


@mock.patch('app.get_db')
def test_positions(mock_get_db):
    cursor = simple_db()
    mock_get_db.return_value = cursor
    response = app.app.test_client().get('/api/positions/9632179/')
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    expected = [
        {'latitude': 51.8, 'longitude': 2.7, 'timestamp': '2019'},
        {'latitude': 51.8, 'longitude': 2.7, 'timestamp': '2018'},
        {'latitude': 51.8, 'longitude': 2.7, 'timestamp': '2017'},
    ]
    assert data == expected


@mock.patch('app.get_db')
def test_positions_bad_input(mock_get_db):
    cursor = simple_db()
    mock_get_db.return_value = cursor
    response = app.app.test_client().get('/api/positions/000000000/')
    assert response.status_code == 404

