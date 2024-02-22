# EC530-flaskrestful-demo
This GitHub repo is meant to provide you all with some simple demos for using Flask-RESTful for implementing your own REST API. All 3 of the demos use a simple example of using a REST API for storing, retrieving, and deleting data about users (basically, using the Flask REST API to store user information and perform CRUD operations on them).

Each of the demos has 2 main python scripts:
1. **app.py**: The Flask REST API server script. Running this script will start the Flask REST API to run on localhost:5000
2. **client.py**: A simple script made for interacting with the Flask REST API as it's running (perform GET, PUT, and DELETE functions)

### Installation:
```
git clone https://github.com/TrevorChan1/EC530-flaskrestful-demo.git
cd EC530-flaskrestful-demo
pip3 install -r requirements.txt
```

### Example Running it:
```
cd EC530-flaskrestful-demo
# Run the Flask REST API server
python3 ./app.py

# On a separate terminal, run the following to interact with the server
python3 ./client.py
```

## Demo 1: simple_demo
This demo is the most simple and just contains a very minimal, bare-bones Flask REST API implementation. This just initializes a Flask REST API to run on the localhost:5000/user/<user_id> URL, attaches basic functions for setting, getting, and deleting users.

## Demo 2: demo_data_cleaning
This demo is the same as demo 1, but incorporates response marshalling and request parsing to demonstrate how to ensure the data you send / receive is in the expected format

## Demo 3: demo_with_database
This demo is the same as demo 2, but incorporates Flask's SQLAlchemy library so that information will exist beyond the server session. This is meant to hopefully give a useful example on how to create and use a database in a REST API implementation for your homework this week.