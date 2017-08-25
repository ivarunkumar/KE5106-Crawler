from Persistence import DataManager
import SentimentAnalysis as SA
from TaskManager import TaskManager

def patch():
    dm = DataManager()
     
    out = dm.readReviewsLimited({"sentimentScore.label": "NA"})
    for rec in out :
        res = SA.GetSentimentAnalysis(rec["reviewText"])
        label = "NA"
        pos = neg = neu = 0.0
        if res != None :
            data = res.json()
            label = data['label']
            neg = data['probability']['neg']
            neu = data['probability']['neutral']
            pos = data['probability']['pos']
        print(rec["_id"])
        dm.updateReview({"_id" : rec["_id"]}, {"$set" : {"sentimentScore": {"label" : label, "positive" : pos, "negative" : neg, "neutral" : neu}}})



if __name__ == '__main__':
    patch()