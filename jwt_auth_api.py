from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity


app = Flask(__name__)
# TODO: SECRET_KEY - digitally-sign for the JWT token. This needs to be more difficult. Maybe a random generated string?
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app, prefix="/api/v1")


class User(object):
    """
    Represents the "identity" of a user of the API.

    Currently hard codes a "database" of users (user_data dict). LDAP integration here???
    """
    def __init__(self, id):
        self.id = id
        # self.username = username
        # self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

user_data = {
    "andrew": "spizzle83"
}


def authenticate(username, password):
    """
    Function for handling API calls to the /auth API.

    This function is called by Flask_JWT to:
     1. Authenticate the user by looking them up in our security database.
     2. validate the password the user passed in matches our database password.
     3. returns a user object so the user identity can be accessed after authentication if needed.

    :param username: username of the API requester
    :param password: password for the user
    :return: User object with a generated ID number for now.
    """
    if not (username and password):
        return False
    if user_data.get(username) == password:
        return User(id=123)


def wng_identity(payload):
    """
    Called by Flask_JWT to look up a user by their ID and return the user object.
    :param payload:
    :return:
    """
    user_id = payload['identity']
    return {'user_id': user_id}

jwt = JWT(app, authentication_handler=authenticate, identity_handler=wng_identity)


class PrivateResource(Resource):
    @jwt_required()
    def get(self):
        return dict(current_identity)


# Add resources to API
api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)


