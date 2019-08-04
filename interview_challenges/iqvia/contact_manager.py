from flask import Flask, request, abort, jsonify
import json
from sqlalchemy import create_engine, exc, orm

from contact_model import Base, Contact, Email


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

engine = create_engine(
    'sqlite:///contact_manager.db',
    connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
Base.metadata.bind = engine
 
DBSession = orm.sessionmaker(bind=engine)
session = DBSession()


def get(key, entity):
    """ Generic get 
    
        key: a contact's username or email address
        entity: Contact or Email class
    """
    obj = session.query(entity).get(key)
    if not obj:
        abort(404, '{} not found'.format(key))
    return jsonify(obj.to_dict())


@app.route('/api/get/contact/<username>', methods=['GET'])
def get_contact(username):
    return get(username, Contact)


@app.route('/api/get/email/<address>', methods=['GET'])
def get_email(address):
    return get(address, Email)


def gets(entity):
    return jsonify([o.to_dict() for o in session.query(entity).all()])

@app.route('/api/get/contacts', methods=['GET'])
def get_contacts():
    return gets(Contact)


@app.route('/api/get/emails', methods=['GET'])
def get_emails():
    return gets(Email)


def create(obj_factory):
    """ Generic create which handles the HTTP response and DB but gives the 
        request's json to obj_factory to build the particular object
    """
    if not request.json:
        abort(400, 'Bad request')
    obj = obj_factory(request.json)
    session.add(obj)
    try:
        session.commit()
    except exc.InvalidRequestError as err:
        app.logger.error('InvalidRequestError: Failed to create %s', 
            obj.to_dict())
        session.rollback()
        session.flush()
        return abort(500, 'Invalid request error')
    return request.json, 201


@app.route('/api/create/contact', methods=['POST'])
def create_contact():
    """
    For contact, the request json should be like so:
        {
            'username': 'anna',
            'first_name': 'Anna',
            'last_name': 'Zander'
        }
        
    """
    def make_contact(req_json):
        return Contact(
            username=req_json['username'],
            first_name=req_json['first_name'],
            last_name=req_json['last_name'])

    return create(make_contact)


@app.route('/api/create/email', methods=['POST'])
def create_email():
    """
    The request json should be like so:
        {
            'username': 'anna',
            'address': 'anna@cisco.com'
        }

    """
    def make_email(req_json):
        contact = session.query(Contact).get(req_json['username'])
        return Email(
            address=req_json['address'],
            contact=contact)

    return create(make_email)


def delete(key, entity):
    obj = session.query(entity).get(key)
    if not obj:
        abort(400, 'Invalid key')
    session.delete(obj)
    session.commit()
    return json.dumps({'result': True})


@app.route('/api/delete/contact/<username>', methods=['DELETE'])
def delete_contact(username):
    return delete(username, Contact)


@app.route('/api/delete/email/<address>', methods=['DELETE'])
def delete_email(address):
    return delete(address, Email)


# No update for email - it's too short - delete and create a new one.
@app.route('/api/update/contact/<username>', methods=['PUT'])
def update_contact(username):
    """
    For username anna, the request json should have one or both fields
        {
            'first_name': 'Anna',
            'last_name': 'Zander'
        }

    """
    contact = session.query(Contact).get(username)
    if not contact:
        abort(400, 'Bad key')
    contact.first_name = request.json.get('first_name', contact.first_name)
    contact.last_name = request.json.get('last_name', contact.last_name)
    session.commit()
    return jsonify(contact.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
