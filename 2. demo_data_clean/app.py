from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with, reqparse

# demo_with_database: A more complex demo

# Define flask app and flask_restful API objects
app = Flask(__name__)
api = Api(app)

# NEW: Adding in definitions for how request inputs should be defined
user_definition = {
    'user_id' : fields.Integer,
    'name' : fields.String,
    'secret' : fields.String
}

class FormatUser(object):
    def __init__(self, uid, name, secret):
        self.user_id = uid
        self.name = name
        self.secret = secret

users = {
    2 : {'name' : 'Trevor', 'secret' : 'I thought WiFi was powered by satellites until I was 20'}
}

# NEW: Define a request parser that looks for the specific required arguments
parser = reqparse.RequestParser()
parser.add_argument('name', help="Name cannot be blank")
parser.add_argument('secret', required=True, help="Secret cannot be blank")

def get_user(user_id):
    # If find user, return
    if (users.get(user_id)):
        user_info = users[user_id]
        return FormatUser(user_id, user_info['name'], user_info['secret'])
    # Otherwise, send error message and error code
    else:
        return {'error' : 'no such user found'}, 404

# Define a Resource-type class object to define functions for the RESTful API
class UserAPI(Resource):

    # Under resource objects, you can define functions corresponding to HTTP requests
    # i.e. GET, POST, DELETE, etc.

    # GET function, which defines what is sent to the user-side from the server
    # NEW: marshal_with will serialize the API response to follow schema
    @marshal_with(user_definition)
    def get(self, user_id):
        return get_user(user_id)
    
    # PUT / POST function, where you are able to access the request value and store it on the server-side
    @marshal_with(user_definition)
    def post(self, user_id):
        
        # NEW: Adding in flask request parsing
        try:
            args = parser.parse_args()

            users[user_id] = {'name' : args['name'], 'secret' : args['secret']}
            return FormatUser(user_id, args['name'], args['secret'])
        except Exception as e:
            print(e)
            return e, 500

    # DELETE function for deleting resources from the API
    def delete(self, user_id):
        if (users.get(user_id)):
            del users[user_id]
        else:
            return {'error' : 'no such user found'}, 404
        return
    

# Use the API object to connect the Resource objects to paths on the Flask server
# Once running the app, can test that it's working: curl http://127.0.0.1:5000
# Example PUT curl http://localhost:5000/todo1 -d "data=Remember the milk" -X PUT
    
# /<datatype: input_name> = a way to have variable paths
api.add_resource(UserAPI, '/user/<int:user_id>')

if __name__ == '__main__':
    app.run()