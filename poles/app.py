import csv
import flask
import operator
import sqlite3


app = flask.Flask(__name__)


@app.route('/api/ships/')
def ships():
    cursor = get_db()
    result = []

    for ship in cursor.execute('select * from Ships'):
        result.append({'name': str(ship[0]), 'imo': str(ship[1])})

    return flask.jsonify(result)


@app.route('/api/positions/<imo>/')
def positions(imo):
    cursor = get_db()
    result = []

    for p in cursor.execute('select * from Positions where imo = "%s"' % imo):
        result.append({
            'timestamp': p[1],
            'latitude':  p[2],
            'longitude': p[3]
        })

    if not result:
        flask.abort(404)

    return flask.jsonify(sorted(result, key=operator.itemgetter('timestamp'),
        reverse=True))


def _build_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    c.execute('''create table Ships (name text, imo integer)''')
    c.execute('''create table Positions (
                    imo integer,
                    timestamp text,
                    latitude real,
                    longitude real)''')

    conn.commit()
    return conn


def fill_db(positions_file):
    conn = _build_db()
    cursor = conn.cursor()

    ships = [('Mathilde Maersk', 9632179),
             ('Australian Spirit', 9247455),
             ('MSC Preziosa', 9595321)]
    for ship in ships:
        cursor.execute('insert into Ships values ("%s", %s)' % ship)

    for row in csv.reader(positions_file):
        cursor.execute('''insert into Positions values (%s, "%s", %s, %s)''' %
                            tuple(row))

    conn.commit()
    return cursor


def get_db():
    if 'db' not in flask.g:
        cursor = fill_db(open('positions.csv'))
        flask.g.db = cursor

    return flask.g.db


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
