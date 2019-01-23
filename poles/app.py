import csv
from flask import Flask, g, jsonify
import sqlite3


app = Flask(__name__)

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

@app.route('/api/ships/', methods=['GET'])
def ships():
    cursor = conn.cursor()
    ships = cursor.execute('select * from Ships')

    return jsonify({'ships': ships})


@app.route('/api/positions/{imo}', methods=['GET'])
def positions(imo):
    return []


def build_db():
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


def fill_db(conn, positions_file):
    cursor = conn.cursor()
    cursor.execute('insert into Ships values ("Mathilde Maersk", 9632179)')
    cursor.execute('insert into Ships values ("Australian Spirit", 9247455)')
    cursor.execute('insert into Ships values ("MSC Preziosa", 9595321)')

    for row in csv.reader(positions_file):
        cursor.execute('''insert into Positions values (%s, "%s", %s, %s)''' %
                            tuple(row))

    conn.commit()


def main():
    conn = build_db()
    fill_db(conn, open('positions.csv'))

    app.run(debug=True)


if __name__ == '__main__':
    main()
