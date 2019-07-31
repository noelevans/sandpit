from flask import Flask, jsonify, make_response, request, abort
import json
import redis


app = Flask(__name__)
rdb = redis.StrictRedis(
    db=0, 
    charset='utf-8', 
    decode_responses=True)


@app.route('/api/get/<key>', methods=['GET'])
def get(key):
    response = rdb.get(key)
    if not response:
        return abort(404, '{} not found'.format(key))
    return response


@app.route('/api/get_all/<entity>', methods=['GET'])
def get_all(entity):
    keys = rdb.scan_iter('{}:*'.format(entity)) or []
    entities = [json.loads(rdb.get(k)) for k in keys]
    return jsonify(entities)


@app.route('/api/create/<key>', methods=['POST'])
def create(key):
    if not request.json:
        abort(400, 'Bad request')
    value = json.dumps({
        jk: request.json[jk] for jk in request.json.keys()})
    rdb.set(key, value)
    return value, 201


@app.route('/api/delete/<key>', methods=['DELETE'])
def delete_contact(key):
    count = rdb.delete([key])
    if not count:
        return make_response(
            jsonify({'error': 'Non-existant key'}), 409)
    return json.dumps({'result': True})


@app.route('/api/update/<key>', methods=['PUT'])
def update(key):
    old_value = json.loads(rdb.get(key))
    value = json.dumps({
        jk: request.json[jk] for jk in request.json.keys()})
    rdb.set(key, value)
    return value


if __name__ == '__main__':
    app.run(debug=True)
