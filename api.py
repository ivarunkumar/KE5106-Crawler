from bson import json_util
from flask import Flask, jsonify, request, json
from pymongo import MongoClient
from ModelRunner import runModelForEntity, runModelForReviewer

app = Flask(__name__)


@app.route('/reviewer/<username>',methods=['GET'])
def getReviewerRating(username):
    print('----------------------')
    result = runModelForReviewer(username)
    return jsonify(rating=result)

@app.route('/entity/<entityId>',methods=['GET'])
def getEntityRating(entityId):
    result = runModelForEntity(entityId)
    return jsonify(rating=result)
    
if __name__ == '__main__':
    app.run(debug=True)