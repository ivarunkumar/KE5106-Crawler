from bson import json_util
from flask import Flask, jsonify, request, json
from pymongo import MongoClient
from ModelRunner import runModelForEntity, runModelForReviewer

app = Flask(__name__)


@app.route('/read',methods=['GET'])
def read():
    print('----------------------')
    print(request.args.get('username'))
    username =request.args.get('username')

    #connection = MongoClient('localhost', 27017)  # Connect to mongodb
    #print(connection.database_names())  # Return a list of db, equal to: > show dbs
    #db = connection['TripAdvisor']  # equal to: > use testdb1
    #print("posts" in db.collection_names())  # Check if collection "posts"
    # collection = db['Reviewers']

    result = runModelForReviewer(username)


    return jsonify(data=result)


if __name__ == '__main__':
    app.run(debug=True)