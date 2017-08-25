from pymongo import MongoClient, errors
import json
from Persistence import DataManager
from FetchReviewers import reviewTaskMgr
from pymongo.cursor import Cursor
from MLModel_SVM import fML_SVM_Load_TestModel

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
  
  
def prepareModelInputByReviewer(reviewerId): 
    return prepareModelInput({"userName" : reviewerId})
                       
def prepareModelInput(condition):
    dataMgr = DataManager()
    reviewers = dataMgr.getAllReviewers(condition)
    trainingData = []
    for reviewer in reviewers :
        predictors = []
        reviewerModel1 = [
        #print(
            #reviewer["userName"],
            reviewer["memberSince"], 
            reviewer["ageGroup"],
            reviewer["gender"],
            #reviewer["homeTown"],
            reviewer["points"],
            reviewer["rating"],
            reviewer["badge"]["totalBadges"],
            reviewer["ratingDistribution"]["excellent"],
            reviewer["ratingDistribution"]["veryGood"],
            reviewer["ratingDistribution"]["average"],
            reviewer["ratingDistribution"]["poor"],
            reviewer["ratingDistribution"]["terrible"]
            ]
        
        predictors.extend(reviewerModel1)
        reviewerTransformedOut = dataMgr.getReviewerTransformed(reviewer["userName"])
        reviewerModel2= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        if (reviewerTransformedOut != None):
            for reviewerTransformed in reviewerTransformedOut :
            #reviewerTransformed = reviewerTransformedOut.reviewerTransformedOut.next()
                reviewerModel2 = [
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
                    ]
        predictors.extend(reviewerModel2)
        reviewerAggrOut = dataMgr.getReviewerAggregate(reviewer["userName"])
        reviewerModel3=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if (reviewerAggrOut != None):
            for reviewerAggr in reviewerAggrOut :
                reviewerModel3 = [
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
                ]
        predictors.extend(reviewerModel3)
        #print (predictors)
        print(predictors)
        print ("Num Reviews", predictors[30], "Num Helpful", predictors[31])
        Y=0
        if (predictors[30] != 0) :
            Y=predictors[31]/ predictors[30]
        print (Y)
        aCase = {}
        aCase["predictors"]=predictors
        aCase["class"] =  Y
        trainingData.append(aCase)
    #dataMgr.disconnect()
    return trainingData

def runModelForReviewer(reviewerId): 
    out = prepareModelInputByReviewer(reviewerId)
    result = fML_SVM_Load_TestModel(out[0]["predictors"])
    return result
          
def runModelForEntity(entityId):
    dataMgr = DataManager()
    reviewers = dataMgr.getAllReviewers({"entityId" : entityId})
    result = []
    for reviewer in reviewers :
        out = prepareModelInputByReviewer(reviewer["userName"])
        result.extend(out)
        ### TODO : do math here!
    return result
              
if __name__ == '__main__':
    #getReviewsByEntity("d2439664")
    #getReviewsAndReviewer("MisterGong")
    #out = prepareModelInputByReviewer("MisterGong")
    out = prepareModelInput("MisterGong")
    print("----------------------")
    print(out)
