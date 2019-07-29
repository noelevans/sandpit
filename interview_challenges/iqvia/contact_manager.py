from collections import namedtuple
from flask import Flask, jsonify, make_response, request, abort
import json
import redis


app = Flask(__name__)


def get_db():
    return redis.StrictRedis(db=0)


@app.route('/api/contact/<username>', methods=['GET'])
def get_contact(username):
    response = get_db().get(username)
    if response:
        return json.loads(response)
    return abort(404, 'User not found')


@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    keys = get_db().scan_iter('user:*')
    return jsonify({json.loads(get_db().get(k)) for k in keys})


@app.route('/api/contact', methods=['POST'])
def create_contact():
    contact = json.dumps({
        'username': request.json['username'],
        'email': request.json['email'],
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name']
    })
    get_db().set(username, contact)
    return contact, 201


@app.route('/api/contact/<username>', methods=['DELETE'])
def delete_contact(username):
    count = get_db().delete([username])
    if count:
        return json.dumps({'result': True})
    return make_response(jsonify({'error': 'Non-existant username'}), 409)


@app.route('/api/contact/<username>', methods=['PUT'])
def update_contact(username):
    old_data = get_contact(username)
    new_username = request.json.get('username', username)
    if new_username != username:
        delete_contact(username)
    
    contact = json.dumps({
        username:new_username,
        email:request.json.get('email', old_data.email),
        first_name:request.json.get('first_name', old_data.first_name),
        last_name:request.json.get('last_name', old_data.last_name)
    })
    get_db().set(new_username, contact)
    return contact

