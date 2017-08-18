import re
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import pprint
from time import sleep
from TaskManager import TaskManager, Task
import SentimentAnalysis as SA
import threading

def getReviewDetails(args):
    print("@getReviewDetails", threading.currentThread().getName(), args)
    p_loc = args [0]
    p_title = args [1] 
    p_title='https://www.tripadvisor.com.sg'+p_title
    html_title = requests.get(p_title)
    soup = BS(html_title.content, 'html.parser')
    # Part One
    fullreviewContainer = soup.find('div', {'class':'innerBubble'})
    reviewid=fullreviewContainer.find('p')['id']
    reviewid=reviewid.strip()
    #review=fullreviewContainer.findAll('p', {'property':'reviewBody'}) #not all review has this tag
    review=fullreviewContainer.findAll('div', {'class':'entry'})
    review=review[0].text.strip()
    r = SA.GetSentimentAnalysis(review)
    data = r.json()
    label = data['label']
    neg = data['probability']['neg']
    neu = data['probability']['neutral']
    pos = data['probability']['pos']
    print(label, neg, neu, pos)
    # Part Two
    HeaderContainer = soup.find('h1', {'id':'HEADING'})
    reviewtitle=HeaderContainer.find('div',{'id':'PAGEHEADING'})
    reviewtitle=reviewtitle.text.strip()
    reviewentity=HeaderContainer.find('a',{'href':p_loc})
    reviewentity=reviewentity.text.strip()
    # Part Three
    LocContainer = soup.findAll('span',{'class':'format_address'})
    l_LocContainer=len(LocContainer)
    if l_LocContainer > 0:
        reviewloc=LocContainer[0].text.split()
        reviewloc=reviewloc[-1].strip()
        re.sub(r'\(.*?\)', '',reviewloc)
    elif l_LocContainer == 0:
        reviewloc = 'NA'        
    reviewOut = (reviewid,reviewloc,reviewentity,reviewtitle,review,r)
    print ("@getReviewDetails", reviewOut)        
    return reviewOut 

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
    print("@getMemberReviews", threading.currentThread().getName())
    html = requests.get(input)
    soup = BS(html.content, 'html.parser')
    reviewContainer = soup.findAll('button', {'class':'cs-paginate-goto'})
    size = len(reviewContainer)
    pages = int(reviewContainer[size-1].text) #get num of pages
    #driver = webdriver.PhantomJS()
    driver = webdriver.Chrome()
    #executable_path=r"chromedriver.exe")    
    driver.get(input)
    #html = requests.get(input)
    #soup = BS(html.content, 'html.parser')
    #reviewContainer = soup.findAll('li', {'class':'cs-review'})
    
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
            location = reviewContainer[i].find('div', {'class':'cs-review-location'})
            title = reviewContainer[i].find('a', {'class':'cs-review-title'})
            date = reviewContainer[i].find('div', {'class': 'cs-review-date'})
            rating = reviewContainer[i].find('div', {'class': 'cs-review-rating'})
            votes = reviewContainer[i].find('div', {'class': 'cs-review-helpful-votes'})
            if(votes): #class will not appear if no votes
                vote = votes.text.strip()
            else:
                vote = 0
            points = reviewContainer[i].find('div', {'class': 'cs-points'})
            i_loc= location.find('a')['href']
            i_title=title['href']
            print ("@getMemberReviews >>>> ", i_loc, i_title)
        next_page_elem = driver.find_element_by_id('cs-paginate-next')
        next_page_link = pageSoup.find('button', text='%d' % pageCount)
        
        if next_page_link and pageCount < 3:
            next_page_elem.click()
            pageCount += 1
            sleep(1)
        else:
            print ("********* REMOVE PAGE LIMIT *********** ")
            break
    driver.quit()
    return (jsonMemberReviewList)
    #return (jsonMemberReviewList,jsonDetailsReviewList)
    return None

def getReviewDetailsCallBack(futureObj) :
    print("@getReviewDetailsCallBack", threading.currentThread().getName(), futureObj.result())


def getMemberReviewsCallback(futureObj) :
    reviewdetails = futureObj.result()
    print("@getMemberReviewsCallback", threading.currentThread().getName(), reviewdetails)
    r = reviewdetails[5]
    data = r.json()
    Review = {"ReviewCategory" : getReviewCategory(location),
                "ReviewID" : reviewdetails[0],
                "ReviewDate" : date.text.strip(),
                "ReviewRating" : getReviewRating(rating),
                "ReviewVotes" : vote,
                "ReviewPoints" : points.text,
                "ReviewLocation" : reviewdetails[1],
                "ReviewEntity" : reviewdetails[2],
                "ReviewTitle" : reviewdetails[3],
                "Review" : reviewdetails[4],
                "Sentiment:" : [{
                        "Label" : data['label'],
                        "Pos" : data['probability']['pos'],
                        "Neutral" : data['probability']['neutral'],
                        "Neg" : data['probability']['neg']}],
                     }
    #jsonMemberReviewList.append(Review)
            
     #     pprint.pprint(MemberReviewData)
    #     pprint.pprint(DetailsReviewData)
    #     print('reviewList: ' + str(len(MemberReviewData)))
    #     print('reviewList: ' + str(len(DetailsReviewData)))


#result = getMemberReviews('https://www.tripadvisor.com.sg/members/vykye2000')

