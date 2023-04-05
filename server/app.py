from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        query = Message.query.all()
        all_messages = []
        for message in query:
            all_messages.append(message.to_dict())
        res = make_response(jsonify(all_messages), 200)
        return res
    elif request.method == 'POST':
        print(request.get_json()['body'])
        new_message = Message(
            body = request.get_json()['body'],
            username = request.get_json()['username']
        )
        db.session.add(new_message)
        db.session.commit()
        print(new_message.body)
        res = make_response(new_message.to_dict(), 201)
        return res
        


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'DELETE':
        query = Message.query.filter(Message.id == id).first()
        db.session.delete(query)
        db.session.commit()
        res = make_response({
            'message': 'message deleted.'
        }, 200)
        return res
    if request.method == 'PATCH':
        query = Message.query.filter(Message.id == id).first()
        for attr in request.get_json():
            setattr(query, attr, request.get_json()[attr])
        db.session.add(query)
        db.session.commit()
    response = make_response(query.to_dict(), 200)
    return response


if __name__ == '__main__':
    app.run(port=5555)
