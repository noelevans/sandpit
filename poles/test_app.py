import pytest

import app


def test_fill_db():
    conn = app.build_db()
    cursor = conn.cursor()
    app.fill_db(conn, open('positions.csv'))

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


