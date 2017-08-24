from pymongo import MongoClient, errors
import json
from Persistence import DataManager
from FetchReviewers import reviewTaskMgr

def getReviewsByEntity(entityId) :
    dataMgr = DataManager()
    out = dataMgr.readReviews({"sentimentScore.label" : {"$ne": "NA"}, "entityId" : entityId})
    for o in out:
        print (o["_id"])

def getReviewsAndReviewer(reviewerId):
    dataMgr = DataManager()
    out = dataMgr.getReviewsAndReviewer(reviewerId)
    for o in out:
        print (o["entityName"])
  
  
def prepareModel():
    predictors = []
    
    dataMgr = DataManager()
    reviewers = dataMgr.getAllReviewers()
    #reviewers = dataMgr.getReviewer("rearcardoor") 
    for reviewer in reviewers :
        #reviewerModel1 = [
        print(
            reviewer["userName"],
            reviewer["memberSince"], 
            reviewer["ageGroup"],
            reviewer["gender"],
            reviewer["homeTown"],
            reviewer["points"],
            reviewer["rating"],
            reviewer["badge"]["totalBadges"],
            reviewer["ratingDistribution"]["excellent"],
            reviewer["ratingDistribution"]["veryGood"],
            reviewer["ratingDistribution"]["average"],
            reviewer["ratingDistribution"]["poor"],
            reviewer["ratingDistribution"]["terrible"])
        
        #predictors.append(reviewerModel1)
        reviewerTransformedOut = dataMgr.getReviewerTransformed(reviewer["userName"])
        for reviewerTransformed in reviewerTransformedOut :
            #reviewerModel2 = [
            print(
                int(reviewerTransformed["TS_ArtAndArchitecture_Ind"]), 
                int(reviewerTransformed["TS_Foodie_Ind"]), 
                int(reviewerTransformed["TS_HistoryBuff_Ind"]), 
                int(reviewerTransformed["TS_Nature_Ind"]), 
                int(reviewerTransformed["TS_UrbanExplorer_Ind"]), 
                int(reviewerTransformed["TS_Backpacker_Ind"]), 
                int(reviewerTransformed["TS_BeachGoer_Ind"]), 
                int(reviewerTransformed["TS_Ecotourist_Ind"]), 
                int(reviewerTransformed["TS_LikeALocal_Ind"]), 
                int(reviewerTransformed["TS_PeaceQuietSeeker_Ind"]), 
                int(reviewerTransformed["TS_Thrifty Traveller_Ind"]), 
                int(reviewerTransformed["TS_ThrillSeeker_Ind"]), 
                int(reviewerTransformed["TS_Trendsetter_Ind"]), 
                int(reviewerTransformed["TS_FamilyHolidayMaker_Ind"]), 
                int(reviewerTransformed["TS_LuxuryTraveller_Ind"]), 
                int(reviewerTransformed["TS_NightlifeSeeker_Ind"]), 
                int(reviewerTransformed["TS_Vegetarian_Ind"]), 
                int(reviewerTransformed["TS_ShoppingFanatic_Ind"]), 
                int(reviewerTransformed["TS_60PlusTraveller_Ind"])             
            )
            #predictors.append(reviewerModel2)

        reviewerAggrOut = dataMgr.getReviewerAggregate(reviewer["userName"])
        for reviewerAggr in reviewerAggrOut :
            #reviewerModel3 = [
            print(
                int(reviewerAggr["num_reviews"]),
                int(reviewerAggr["num_helpful"]),
                int(reviewerAggr["Cat_AttractiveReview_Ind"]),
                int(reviewerAggr["Cat_RestaurantReview_Ind"]),
                int(reviewerAggr["Cat_HotelReview_Ind"]),
                int(reviewerAggr["Cat_AirlineReview_Ind"]),
                int(reviewerAggr["Cat_NULL_Ind"]),
                int(reviewerAggr["SS_Pos_Ind"]),
                int(reviewerAggr["SS_Neg_Ind"]),
                int(reviewerAggr["SS_Neutral_Ind"]),
                int(reviewerAggr["SS_NA_Ind"])
            )
            #predictors.append(reviewerModel3)
        #print (predictors)
        print()
          
if __name__ == '__main__':
    #getReviewsByEntity("d2439664")
    #getReviewsAndReviewer("MisterGong")
    prepareModel()
    
    
    
    
