from pymongo import MongoClient, errors
import json

class DataManager :
    mongoClient = MongoClient()
    tripAdvisorDB = mongoClient.get_database(name = "TripAdvisor")
    def __init__ (self) :
        pass
    
    def saveReview (self, review) :
        try:
            print ("@saveReview", review)
            DataManager.tripAdvisorDB.Reviews.insert_one(review)
        except errors.DuplicateKeyError as e:
            print(e)

    def saveReviews (self, reviews) :
        try:
            print ("@saveReviews", reviews)
            DataManager.tripAdvisorDB.Reviews.insert_many(reviews)
        except errors.DuplicateKeyError as e:
            print(e)
        
    def saveReviewer (self, reviewer) :
        try:
            print ("@saveReview", reviewer)
            DataManager.tripAdvisorDB.Reviewers.insert_one(reviewer)
        except errors.DuplicateKeyError as e:
            print(e)

    def saveReviewers (self, reviewers) :
        try:
            print ("@saveReviewers", reviewers)
            DataManager.tripAdvisorDB.Reviewers.insert_many(reviewers)          
        except errors.DuplicateKeyError as e:
            print(e)
        
    def saveEntity (self, entity) :
        try:
            print ("@saveEntity", entity)
            DataManager.tripAdvisorDB.Entities.insert_one(entity)
        except errors.DuplicateKeyError as e:
            print(e)

    def readReviews(self, condition): 
        result = DataManager.tripAdvisorDB.Reviews.find(condition)
        return result
 
    def readReviewsLimited(self, condition): 
        result = DataManager.tripAdvisorDB.Reviews.find(condition).limit(1000)
        return result
      
    def getReviewsAndReviewer(self, reviewerId):
        out = DataManager.tripAdvisorDB.Reviews.aggregate([
            {"$match": {"sentimentScore.label": {"$ne":"NA"}}},
            {"$match": {"reviewerId" : reviewerId}},
            {"$lookup" : {"from":"Reviewers","localField":"reviewerId", "foreignField" : "userName", "as" : "reviewer" }}
            ])
        
        return out
    
    def getReviewer(self, reviewerId): 
        result = DataManager.tripAdvisorDB.Reviewers.find({"userName" : reviewerId})
        return result
    
    def getAllReviewers (self, condition):
        return DataManager.tripAdvisorDB.Reviewers.find(condition)   
    
    def getReviewerTransformed(self, reviewerId):
        return DataManager.tripAdvisorDB.ReviewersTransform.find({"_id" : reviewerId}) 

    def getReviewerAggregate(self, reviewerId):
        return DataManager.tripAdvisorDB.ReviewsAggr.find({"_id" : reviewerId}) 
    
    def disconnect(self): 
        DataManager.mongoClient.close() 
        
        
    def updateReview (self, condition, updateStmt) :
        try:
            print ("@update", condition, updateStmt)
            DataManager.tripAdvisorDB.Reviews.update_one(condition, updateStmt, upsert=False)
        except errors.DuplicateKeyError as e:
            print(e)
