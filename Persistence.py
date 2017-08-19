from pymongo import MongoClient
import json

class DataManager :
    tripAdvisorDB = MongoClient().get_database(name = "TripAdvisor")
    def __init__ (self) :
        pass
    
    def saveReview (self, review) :
        print ("@saveReview", review)
        DataManager.tripAdvisorDB.Reviews.insert_one(review)

    def saveReviews (self, reviews) :
        print ("@saveReviews", reviews)
        DataManager.tripAdvisorDB.Reviews.insert_many(reviews)
        
    def saveReviewer (self, reviewer) :
        print ("@saveReview", reviewer)
        DataManager.tripAdvisorDB.Reviewer.insert_one(reviewer)

    def saveReviewers (self, reviewers) :
        print ("@saveReviewers", reviewers)
        DataManager.tripAdvisorDB.Reviewers.insert_many(reviewers)          
        
    def saveEntity (self, entity) :
        print ("@saveEntity", entity)
        DataManager.tripAdvisorDB.Entity.insert_one(entity)


