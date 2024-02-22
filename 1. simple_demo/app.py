from flask import Flask, jsonify, request
from flask_restful import Resource, Api

# simple_demo: Demonstration of implementing simple API for getting / setting users

# Define flask app and flask_restful API objects
app = Flask(__name__)
api = Api(app)

users = {}

# Define a Resource-type class object to define functions for the RESTful API
class UserAPI(Resource):

    # Under resource objects, you can define functions corresponding to HTTP requests
    # i.e. GET, POST, DELETE, etc.

    # GET function, which defines what is sent to the user-side from the server
    def get(self, user_id):
        # If find user, return
        if (users.get(user_id)):
            return {user_id : users[user_id]}
        # Otherwise, send error message and error code
        else:
            return {'error' : 'no such user found'}, 404
    
    # PUT / POST function, where you are able to access the request value and store it on the server-side
    def put(self, user_id):
        users[user_id] = request.form['data']
        return {user_id : users[user_id]}

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