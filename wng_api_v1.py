from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

app = Flask(__name__)
wng_api = Api(app=app, prefix="/api/v1")

users = [
    {"email": "masnun@gmail.com", "name": "Masnun", "id": 1}
]

subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument('name', type=str, required=True, help='Name has to be valid string')
subscriber_request_parser.add_argument('email', required=True)
subscriber_request_parser.add_argument('id', type=int, required=True, help='Please enter valid integer as ID')

def get_user_by_id(user_id):
    """
    Gets a users information by ID number and returns it.
    :param user_id: ID of the user to get from the users list.
    :return:
    """
    for x in users:
        if x.get("id") == int(user_id):
            return x


class SubscriberCollection(Resource):
    def get(self):
        """

        :return:
        """
        return users

    def post(self):
        """
        cURL POST data -  curl -d "name=andrew&email=andrew@outlook.com&id=2" http://127.0.0.1:5000/api/v1/subscribers
        cURL POST JSON data -  curl -H "content-type:application/json" -X post -d '{"name":"Jim","email":"jim@hotmail.com","id":"3"}' http://127.0.0.1:5000/api/v1/subscribers

        :return:
        """
        args = subscriber_request_parser.parse_args()
        users.append(args)
        return {"msg": "Subscriber added", "subscriber_data": args}, 201


class Subscriber(Resource):
    def get(self, sub_id):
        """
        curl http://127.0.0.1:5000/api/v1/subscribers/2
        :param sub_id:
        :return:
        """
        user = get_user_by_id(sub_id)
        if not user:
            return {"error": "User not Found"}, 404
        return user

    def put(self, sub_id):
        """
        curl -X PUT -H "Content-Type: application/json" -d '{"name":"Andrew Spear", "email":"Andrew.Spear83@yahoo.com","id":"2"}' http://127.0.0.1:5000/api/v1/subscribers/2
        :param sub_id:
        :return:
        """
        args = subscriber_request_parser.parse_args()
        user = get_user_by_id(sub_id)
        if user:
            users.remove(user)
            users.append(args)
        return args

    def delete(self, sub_id):
        """
        curl -X DELETE http://127.0.0.1:5000/api/v1/subscribers/3
        :param sub_id:
        :return:
        """
        user = get_user_by_id(sub_id)
        if user:
            users.remove(user)
        return {"message": "Deleted"}, 204


wng_api.add_resource(SubscriberCollection, '/subscribers')
wng_api.add_resource(Subscriber, '/subscribers/<int:sub_id>')

if __name__ == '__main__':
    app.run(debug=True)
