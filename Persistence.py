from pymongo import MongoClient
import json

mongoClient = MongoClient()
database = mongoClient.TripAdvisor

def saveReview (review) :
    jsdoc = json.dumps(review)
    print ("@saveReview", jsdoc)
    database.Review.insert_one(jsdoc)

def saveReviews (reviews) :
    jsdocs = json.dumps(reviews)
    database.Review.insert_many(jsdocs)     