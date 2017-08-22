import re
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import pprint
from time import sleep
from TaskManager import TaskManager, Task, BrowserTaskManager
import SentimentAnalysis as SA
import threading
from BadgeInfo import fetchBadgeInfo, fetchBadgeInfoCallback
from Persistence import DataManager

gReviewerTaskMgr = TaskManager("REVIEWER", 10)
gReviewTaskMgr = TaskManager("REVIEWS", 10)

dataManager = DataManager()

def getStrPo(full, sub):
    index = 0
    sub_index = 0
    position = -1
    for ch_i,ch_f in enumerate(full) :
        if ch_f.lower() != sub[sub_index].lower():
            position = -1
            sub_index = 0
        if ch_f.lower() == sub[sub_index].lower():
            if sub_index == 0 :
                position = ch_i

            if (len(sub) - 1) <= sub_index :
                break
            else:
                sub_index += 1

    return position

def getReviewDetails(payload):
    print("@getReviewDetails", threading.currentThread().getName())
    userName = payload["userName"]
    reviewContainer = payload["reviewContainer"]
    location = reviewContainer.find('div', {'class':'cs-review-location'})
    title = reviewContainer.find('a', {'class':'cs-review-title'})
    date = reviewContainer.find('div', {'class': 'cs-review-date'})
    rating = reviewContainer.find('div', {'class': 'cs-review-rating'})
    votes = reviewContainer.find('div', {'class': 'cs-review-helpful-votes'})
    if(votes): #class will not appear if no votes
        vote = votes.text.strip()
    else:
        vote = 0
    points = reviewContainer.find('div', {'class': 'cs-points'})
    i_loc= location.find('a')['href']
    i_title=title['href']
    start = i_title.find('-r') + 1
    end = i_title.find('.html', start)
    test_rid=i_title[start:end]
    rstart = test_rid.find('r')
    rend = test_rid.find('-', rstart)
    if rend==-1:
        rid=i_title.rsplit('-', 1)[1]
    else:
        rid=test_rid[rstart:rend]
    p_title='https://www.tripadvisor.com.sg'+i_title
    html_title = requests.get(p_title)
    soup = BS(html_title.content, 'html.parser')
    fullreviewContainer = soup.find('div', {'class':'innerBubble'})
    if rend == -1 or fullreviewContainer.findAll('div', {'class':'entry'}) is None:
        r='NA'
        review='NA'
        reviewloc='NA'
        label = "NA"
        pos = neg = neu = 0.0
    else:
        # Part One
        #fullreviewContainer = soup.find('div', {'class':'innerBubble'})
        #reviewid=fullreviewContainer.find('p')['id']
        #reviewid=reviewid.strip()
        #review=fullreviewContainer.findAll('p', {'property':'reviewBody'}) #not all review has this tag
        review=fullreviewContainer.findAll('div', {'class':'entry'})
        review=review[0].text.strip()
        r = SA.GetSentimentAnalysis(review)
        label = "NA"
        pos = neg = neu = 0.0
        if r != None :
            data = r.json()
            label = data['label']
            neg = data['probability']['neg']
            neu = data['probability']['neutral']
            pos = data['probability']['pos']
            print(label, neg, neu, pos)
        # Part Two
        #HeaderContainer = soup.find('h1', {'id':'HEADING'})
        #reviewtitle=HeaderContainer.find('div',{'id':'PAGEHEADING'})
        #if (reviewtitle != None) :
        #    reviewtitle=reviewtitle.text.strip()
        #    reviewentity=HeaderContainer.find('a',{'href':i_loc})
        #    reviewentity=reviewentity.text.strip()
        # Part Three
        reviewloc='NA'
        if soup.find('span',{'class':'country-name'}) is None:
            print('NoCountryNameFound')
        else:
            LocContainer = soup.find('span',{'class':'country-name'})
            #print(LocContainer)
            reviewloc=LocContainer.text
    entityId = i_title.split("-")[2]
    reviewDoc = {
        "reviewerId" : userName,
        "entityId" : entityId, 
        "reviewId" : rid,
        "reviewDate" : date.text.strip(),
        "reviewLocation" : reviewloc,
        "category" : getReviewCategory(location),
        "rating" : getReviewRating(rating),
        "points" : points.text.strip(),
        "helpfulVote" : vote,
        "entityName" : location.text,
        "sentimentScore" : {
            "label" : label,
            "positive" : pos,
            "negative" : neg,
            "neutral" : neu
        },
        "reviewText" : review
    }
    
    #reviewOut = (reviewid,reviewloc,reviewentity,reviewtitle,review,r)
    print ("@getReviewDetails", reviewDoc)
    dataManager.saveReview(reviewDoc)        
    return reviewDoc 

def getReviewCategory(location):
    category = 'NULL'
    if('Restaurant_Review' in location.find('a')['href']):
        category = 'Restaurant_Review'
    elif('Attraction_Review' in location.find('a')['href']):
        category = 'Attraction_Review'
    elif('Hotel_Review' in location.find('a')['href']):
        category = 'Hotel_Review'
    elif('Airline_Review' in location.find('a')['href']):
        category = 'Airline_Review'
    return category

def getReviewRating(rating):
    if(rating.find(class_='ui_bubble_rating bubble_5')):
        rating = 5
    elif(rating.find(class_='ui_bubble_rating bubble_4')):
        rating = 4
    elif(rating.find(class_='ui_bubble_rating bubble_3')):
        rating = 3
    elif(rating.find(class_='ui_bubble_rating bubble_2')):
        rating = 2
    elif(rating.find(class_='ui_bubble_rating bubble_1')):
        rating = 1
    else:
        rating = 0
    return rating

def getMemberReviews(input):
    print("@getMemberReviews", threading.currentThread().getName(), input)
    driver = webdriver.Chrome()
    driver.get(input)
    pageSoup = BS(driver.page_source, 'html.parser')
    reviewContainer = pageSoup.findAll('button', {'class':'cs-paginate-goto'})
    size = len(reviewContainer)
    pages = int(reviewContainer[size-1].text) #get num of pages
    userName = input.split("/")[4]
    profileObj = fetchBadgeInfo(pageSoup)
    reviewerDoc = {
        "userName" : userName,
        "memberSince" : profileObj.agesince,
        "ageGroup" : profileObj.age,
        "gender" :  profileObj.sex,
        "homeTown" : profileObj.hometown,
        "points" : profileObj.point,
        "rating" : profileObj.level,
        "travelStyle" : profileObj.tagBlocklist,
        "badge" : {
            "lastBadge" : profileObj.Largebadge,
            "totalBadges" : profileObj.totalBadges
        }
    }
    dataManager.saveReviewer(reviewerDoc)
    
    jsonMemberReviewList = []
    #jsonDetailsReviewList = []
    pageCount = 2
    while(True):#for each page
        #print('page')
        pageSoup = BS(driver.page_source, 'html.parser')
        sleep(1)
        reviewContainer = pageSoup.findAll('li', {'class':'cs-review'})
        reviewSize = len(reviewContainer)
        for i in range(reviewSize):
            print ("@getMemberReviews >>>> ", reviewContainer[i])
            payload = {}
            payload["userName"] = userName
            payload["reviewContainer"] = reviewContainer[i]
            task = Task("MEMBER_REVIEW", getReviewDetails, getReviewDetailsCallback, payload)
            gReviewTaskMgr.addTaskQ(task)
        next_page_elem = driver.find_element_by_id('cs-paginate-next')
        next_page_link = pageSoup.find('button', text='%d' % pageCount)
         
        if next_page_elem : # and pageCount < 3:
            next_page_elem.click()
            pageCount += 1
            sleep(1)
        else:
            print ("********* REMOVE PAGE LIMIT *********** ")
            break
    driver.quit()
    return None

def getReviewDetailsCallback(futureObj) :
    print("@getReviewDetailsCallBack", threading.currentThread().getName(), futureObj.result()["reviewId"] + " saved.")



def getMemberReviewsCallback(futureObj) :
    #Review = futureObj.result()
    print("@getMemberReviewsCallback", threading.currentThread().getName() +" Done")
    #jsonMemberReviewList.append(Review)
            
     #     pprint.pprint(MemberReviewData)
    #     pprint.pprint(DetailsReviewData)
    #     print('reviewList: ' + str(len(MemberReviewData)))
    #     print('reviewList: ' + str(len(DetailsReviewData)))


#result = getMemberReviews('https://www.tripadvisor.com.sg/members/vykye2000')

    
