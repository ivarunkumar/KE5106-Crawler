import requests
import json
import pprint

url = 'http://text-processing.com/api/sentiment/'
input = 'lousy'
def GetSentimentAnalysis(x):
    payload = {'text': x}
    r = requests.post(url, data=payload)
    if r.status_code == 200 :
        return(r)
    else:
        return None

#r = GetSentimentAnalysis(input)
#data = r.json()
#label = data['label']
#neg = data['probability']['neg']
#neu = data['probability']['neutral']
#pos = data['probability']['pos']
#print(label)
#print(neg)
#print(neu)
#print(pos)
#pprint.pprint(r.json())