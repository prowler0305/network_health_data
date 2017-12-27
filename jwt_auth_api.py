from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app, prefix="/api/v1")

user_data = {
    "andrew": "spizzle83"
}


class User(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id='%s')" % self.id


def verify(username, password):
    if not (username and password):
        return False
    if user_data.get(username) == password:
        return User(id=123)


def identity(payload):
    user_id = payload['identity']
    return {'user_id': user_id}


jwt = JWT(app, authentication_handler=verify, identity_handler=identity)


class PrivateResource(Resource):
    @jwt_required()
    def get(self):
        return dict(current_identity)


api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)


