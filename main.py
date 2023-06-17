from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, ime, email):
        self.ime = ime
        self.email = email

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({'id': user.id, 'ime': user.ime, 'email': user.email})
    return jsonify(result)
