from bson import json_util
from flask import Flask, jsonify, request, json
from flask_pymongo import PyMongo
from pymongo import MongoClient
from ModelRunner import runModelForEntity, runModelForReviewer

app = Flask(__name__)
app.config['MONGO_DBNAME'] ='TripAdivor'
app.config['MONGO_URL']='mongodb://localhost:27017/TripAdvisor'

mongo =PyMongo(app)
@app.route('/read/<username>')
def read(username):

    connection = MongoClient('localhost', 27017)  # Connect to mongodb

    print(connection.database_names())  # Return a list of db, equal to: > show dbs

    db = connection['TripAdvisor']  # equal to: > use testdb1
    print("posts" in db.collection_names())  # Check if collection "posts"
    collection = db['Reviewers']

    ff = collection.count()
    result = runModelForReviewer(username)

    #ff = collection.find({"reviewLocation": "Singapore"})
   # ff = collection.find({"userName": "780shivs"})
    print(username)
   # ff = collection.find({"userName": username })

    data = ''
    data =ff

    data = [json.dumps(item, default=json_util.default) for item in ff]
    return jsonify(data=result)
    #return username

@app.route('/test/', methods=['GET'])
def getQ():
    print(request.args.get('a'))
    print(request.args.get('b'))
    return "lalala"


if __name__ == '__main__':
    app.run(debug=True)
