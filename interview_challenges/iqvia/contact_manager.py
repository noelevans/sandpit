from flask import Flask, jsonify, make_response, request, abort
import json
import redis


app = Flask(__name__)
rdb = redis.StrictRedis(db=0)


@app.route('/api/contact/<username>', methods=['GET'])
def get_contact(username):
    response = rdb.get('user:' + username)
    if not response:
        return abort(404, 'User not found')
    return response


@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    keys = rdb.scan_iter('user:*') or []
    contacts = [json.loads(rdb.get(k).decode('utf-8')) for k in keys]
    return jsonify(contacts)


@app.route('/api/contact/create', methods=['POST'])
def create_contact():
    if not request.json or 'username' not in request.json:
        abort(400, 'Bad request')
    contact = json.dumps({
        'username': request.json['username'],
        'email': request.json['email'],
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name']
    })
    rdb.set('user:' + request.json['username'], contact)
    return contact, 201


@app.route('/api/contact/delete/<username>', methods=['DELETE'])
def delete_contact(username):
    count = rdb.delete(['user:' + username])
    if not count:
        return make_response(
            jsonify({'error': 'Non-existant username'}),
            409)
    return json.dumps({'result': True})


@app.route('/api/contact/update', methods=['PUT'])
def update_contact():
    if 'username' not in request.json:
        abort(400, 'Missing username in update')
    username = request.json['username']
    old_data = json.loads(rdb.get('user:' + username))
    contact = json.dumps({
        'username': username,
        'email': request.json.get('email', old_data['email']),
        'first_name': request.json.get('first_name', old_data['first_name']),
        'last_name': request.json.get('last_name', old_data['last_name'])
    })
    rdb.set('user:' + username, contact)
    return contact


if __name__ == '__main__':
    app.run(debug=True)
