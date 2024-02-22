from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
import os

# demo_with_database: A more complex demo

# Define flask app and flask_restful API objects
app = Flask(__name__)
api = Api(app)

# NEW: Configure our app to connect to the database 'database.db' SQLite file (since SQLite db is locally stored)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
db = SQLAlchemy(app)

# NEW: Define our database schema in SQLAlchemy to reflect the database schema defined when creating database.db
# NOTE: This has to connect to an EXISTING SQLite db (it won't create it for you)
# NOTE: Command used to create table in SQLite3:
    # CREATE TABLE users (
    #    id INT PRIMARY KEY,
    #    name TEXT NOT NULL,
    #    secret TEXT NOT NULL);

# NEW: Define the SQLite table schema (with the same name) as a db.Model object
class users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    secret = db.Column(db.String(200), nullable = False)

    def __init__(self, id, name, secret):
        self.id = id
        self.name = name
        self.secret = secret

    # This is the secret sauce that shows what values are returned when this object is queried
    # Doesn't seem like I can make it a dict
    def __repr__(self):
        return self.name



# Define output data schema
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


# Define request parser
parser = reqparse.RequestParser()
parser.add_argument('name', help="Name cannot be blank")
parser.add_argument('secret', required=True, help="Secret cannot be blank")

# NEW: get_user now uses SQLAlchemy rather than the users dict
def get_user(user_id):
    # If find user, return
    user = users.query.filter_by(id=user_id).first()

    try:
        if (user):
            return FormatUser(user.id, user.name, user.secret)
        # Otherwise, send error message and error code
        else:
            return {'error' : 'no such user found'}, 404
    except Exception as e:
        print(e)

# Define a Resource-type class object to define functions for the RESTful API
class UserAPI(Resource):

    # Under resource objects, you can define functions corresponding to HTTP requests
    # i.e. GET, POST, DELETE, etc.

    # GET function, which defines what is sent to the user-side from the server
    # marshal_with will serialize the API response to follow schema
    @marshal_with(user_definition)
    def get(self, user_id):
        return get_user(user_id)
    
    # PUT / POST function, where you are able to access the request value and store it on the server-side
    @marshal_with(user_definition)
    def post(self, user_id):

        # Parse request for desired values name and secret
        try:
            args = parser.parse_args()

            # NEW: Start SQLite db session, insert and commit
            new_user = users(user_id, args['name'], args['secret'])
            db.session.add(new_user)
            db.session.commit()

            return FormatUser(user_id, args['name'], args['secret'])
        except Exception as e:
            print(e)
            return e

    # DELETE function for deleting resources from the API
    def delete(self, user_id):

        # NEW: Use db session to find and delete user
        try:
            user = users.query.filter_by(id=user_id).first()
            if (user):
                db.session.delete(user)
                db.session.commit()
            else:
                return {'error' : 'no such user found'}, 404
        except Exception as e:
            return e
    

# Use the API object to connect the Resource objects to paths on the Flask server
# Once running the app, can test that it's working: curl http://127.0.0.1:5000
# Example PUT curl http://localhost:5000/todo1 -d "data=Remember the milk" -X PUT
    
# /<datatype: input_name> = a way to have variable paths
api.add_resource(UserAPI, '/user/<int:user_id>')

if __name__ == '__main__':
    app.run()