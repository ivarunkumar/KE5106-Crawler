from pymongo import MongoClient, errors
import json
from Persistence import DataManager
from FetchReviewers import reviewTaskMgr
from pymongo.cursor import Cursor
from ML_SVM007 import fML_SVM_Load_TestModel
import datetime

AGE_GROUP = { 
    ""  : 0,
    "13-17" : 1,
    "18-24" : 2,
    "25-34" : 3,
    "35-49" : 4,
    "50-64" : 5,
    "65+":6,
    "| another gender identity" : 0, #fix needed; ignored for now
    "another gender identity" : 0 #fix needed; ignored for now
    }

def getMemberAge(value): 
    if (value == "" or value == None or value == "week") :
        return 0
    
    memSince = int(value)
    now = datetime.datetime.now()
    return (now.year - memSince)
    
     
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
  
    dataMgr.disconnect()
def prepareModelInputByReviewer(reviewerId): 
    return prepareModelInput({"userName" : reviewerId})
                       
def prepareModelInput(condition):
    dataMgr = DataManager()
    reviewers = dataMgr.getAllReviewers(condition)
    trainingData = []
    for reviewer in reviewers :
        predictors = []
        
        gender = 0
        if reviewer["gender"] == "male" : 
            gender = 1
        elif reviewer["gender"] == "female" :
            gender = 2
        
        ageGroup = AGE_GROUP[reviewer["ageGroup"]]
        if ageGroup == None :
            ageGroup = 0
            
        reviewerModel1 = [
        #print(
            #reviewer["userName"],
            getMemberAge(reviewer["memberSince"]), 
            ageGroup,
            gender,
            #reviewer["homeTown"],
            int(reviewer["points"].replace(',','')),
            int(reviewer["rating"]),
            int(reviewer["badge"]["totalBadges"]),
            int(reviewer["ratingDistribution"]["excellent"]),
            int(reviewer["ratingDistribution"]["veryGood"]),
            int(reviewer["ratingDistribution"]["average"]),
            int(reviewer["ratingDistribution"]["poor"]),
            int(reviewer["ratingDistribution"]["terrible"])
            ]
        
        predictors.extend(reviewerModel1)
        reviewerTransformedOut = dataMgr.getReviewerTransformed(reviewer["userName"])
        reviewerModel2= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        if (reviewerTransformedOut != None):
            for reviewerTransformed in reviewerTransformedOut :
                reviewerModel2[0]= int(reviewerTransformed["TS_ArtAndArchitecture_Ind"]) 
                reviewerModel2[1]= int(reviewerTransformed["TS_Foodie_Ind"]) 
                reviewerModel2[2]= int(reviewerTransformed["TS_HistoryBuff_Ind"]) 
                reviewerModel2[3]= int(reviewerTransformed["TS_Nature_Ind"]) 
                reviewerModel2[4]= int(reviewerTransformed["TS_UrbanExplorer_Ind"]) 
                reviewerModel2[5]= int(reviewerTransformed["TS_Backpacker_Ind"]) 
                reviewerModel2[6]= int(reviewerTransformed["TS_BeachGoer_Ind"]) 
                reviewerModel2[7]= int(reviewerTransformed["TS_Ecotourist_Ind"]) 
                reviewerModel2[8]= int(reviewerTransformed["TS_LikeALocal_Ind"]) 
                reviewerModel2[9]= int(reviewerTransformed["TS_PeaceQuietSeeker_Ind"]) 
                reviewerModel2[10]= int(reviewerTransformed["TS_Thrifty Traveller_Ind"]) 
                reviewerModel2[11]= int(reviewerTransformed["TS_ThrillSeeker_Ind"]) 
                reviewerModel2[12]= int(reviewerTransformed["TS_Trendsetter_Ind"]) 
                reviewerModel2[13]= int(reviewerTransformed["TS_FamilyHolidayMaker_Ind"]) 
                reviewerModel2[14]= int(reviewerTransformed["TS_LuxuryTraveller_Ind"]) 
                reviewerModel2[15]= int(reviewerTransformed["TS_NightlifeSeeker_Ind"]) 
                reviewerModel2[16]= int(reviewerTransformed["TS_Vegetarian_Ind"]) 
                reviewerModel2[17]= int(reviewerTransformed["TS_ShoppingFanatic_Ind"]) 
                reviewerModel2[18]= int(reviewerTransformed["TS_60PlusTraveller_Ind"])

            reviewerTransformedOut.close()
        predictors.extend(reviewerModel2)
        reviewerAggrOut = dataMgr.getReviewerAggregate(reviewer["userName"])
        reviewerModel3=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if (reviewerAggrOut != None):
            for reviewerAggr in reviewerAggrOut :
                reviewerModel3[0]=int(reviewerAggr["num_reviews"])
                reviewerModel3[1]=int(reviewerAggr["num_helpful"])
                reviewerModel3[2]=int(reviewerAggr["Cat_AttractiveReview_Ind"])
                reviewerModel3[3]=int(reviewerAggr["Cat_RestaurantReview_Ind"])
                reviewerModel3[4]=int(reviewerAggr["Cat_HotelReview_Ind"])
                reviewerModel3[5]=int(reviewerAggr["Cat_AirlineReview_Ind"])
                reviewerModel3[6]=int(reviewerAggr["Cat_NULL_Ind"])
                reviewerModel3[7]=int(reviewerAggr["SS_Pos_Ind"])
                reviewerModel3[8]=int(reviewerAggr["SS_Neg_Ind"])
                reviewerModel3[9]=int(reviewerAggr["SS_Neutral_Ind"])
                reviewerModel3[10]=int(reviewerAggr["SS_NA_Ind"])
        predictors.extend(reviewerModel3)
        reviewerAggrOut.close()
        Y=0
        if (predictors[30] != 0) :
            Y=predictors[31]/ predictors[30]
        aCase = {}
        aCase["predictors"]=predictors
        aCase["class"] = 0
        if ( Y > 0.3 ) :
            aCase["class"] = 1

        print (aCase)            
        trainingData.append(aCase)
    reviewers.close()
    dataMgr.disconnect()
    return trainingData

def runModelForReviewer(reviewerId): 
    out = prepareModelInputByReviewer(reviewerId)
    result = {"output" : "none"} #fML_SVM_Load_TestModel(out[0]["predictors"])
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
# 
#     out = prepareModelInput({})
#     print("----------------------")
#     X = []
#     Y = []
#     for x in out:
#         print(x)

    #out = prepareModelInputByReviewer("MisterGong")
    out = prepareModelInput({})
    for r in out:
        print("<<<<<", r)
        x= r["predictors"]
        print("running model")
        y = fML_SVM_Load_TestModel(x)
        print("got", y, "actual", r["class"])
      
