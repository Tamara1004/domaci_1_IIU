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

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'ime': user.ime, 'email': user.email})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    ime = data['ime']
    email = data['email']
    user = User(ime, email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    
    data = request.get_json()
    user.ime = data['ime']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
