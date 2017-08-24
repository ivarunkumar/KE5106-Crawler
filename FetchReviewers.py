import sys
# ------- Import Library
import re
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from threading import Timer
from time import sleep
from TaskManager import TaskManager, Task, BrowserTaskManager
from MemberReview import getMemberReviews, getMemberReviewsCallback, gReviewTaskMgr, gReviewerTaskMgr
from Persistence import DataManager
import threading
import unicodedata
#
# ------- Website to Crawl
#gWebTarget = "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d2139448-Reviews-ION_Orchard-Singapore.html"
WEB_TARGET = "https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-Reviews-Universal_Studios_Singapore-Sentosa_Island.html"
DEFAULT_REVIEW_SOURCE_URL = "https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-r***-Universal_Studios_Singapore-Sentosa_Island.html#REVIEWS"
# ------- Selanium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#gSeleniumDriver = webdriver.Chrome(executable_path=r"E:\chromedriver_win32\chromedriver.exe")
#gSeleniumDriver = webdriver.Chrome()


#assert "ION" in gSeleniumDriver.title

# ------- Set Global Variables
gYggdrasil = [] #--- Array container for Parse-Trees

gTaskMgr = TaskManager("REVIEWER")
reviewTaskMgr = TaskManager("REVIEW_INFO")
dataManager = DataManager()

# ------- Function Calls
# HTML Convert to Parse-Tree Search Mark-00
def fMark_00(vUrl, startPageNum, numPages, vParameter1, vParameter2a, vParameter2b) :
    lSeleniumDriver = webdriver.Chrome()
    
    # ------- Total Number of Pages
    gStartPage = startPageNum
    gTotalPages = numPages # 1176 48 pages
    lSeleniumDriver.get(vUrl)
    # empty array list
    vContainer = [] # Multidimensional array # 0 - vOverallRatingContainer, 1 - vMainMemberContainer
    vMainMemberContainer = [] # Multidimensional array
    vOverallRatingContainer = [0,0,0,0,0,0] # 0 - Excellent, 1 - Very good, 2 - Average, 3 - Poor, 4 - Terrible, 5 - Total No Rating
    vMemberContainer = ["","","","",""] # 0 - Display Name, 1 - Username, 2 - Member Profile, 3 - Review Source, 4 - Review Source URL
    #vDefaultReviewSourceURL = "https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-r***-Universal_Studios_Singapore-Sentosa_Island.html#REVIEWS"
    
    #--- Initialisation ---#
    # Downloads the Raw Html Webpage
    vHtml = requests.get(vUrl, timeout=5)
    # r = requests.get(url, headers=headers, timeout=5)
    # Creates a Parse-Tree
    vSoup = BeautifulSoup(vHtml.content, 'html.parser')
    # set-up search container
    vSoupContainer = vSoup.find(vParameter1, {vParameter2a:vParameter2b})
    
    #--- Capture Default Total Reviews ---#
    vDefaultTotalReviews = vSoupContainer.find(string = "Reviews")
    vDefaultTotalReviews = vDefaultTotalReviews.find_parent("span").next_element.next_element.next_element.next_element
    vDefaultTotalReviews = vDefaultTotalReviews[1:-1]
    
    #--- Capture Traveller Ratings (Overall Aggregation) ---#
    # Get List of Traveller Ratings (Overall Aggregation)
    vRatingFilter = vSoupContainer.findAll('div', {'class': 'ui_column is-5 rating'})
    # Get Excellent Rating
    vOverallRatingContainer[0] = vSoupContainer.find(string = "Excellent")
    vOverallRatingContainer[0] = vOverallRatingContainer[0].find_parent("div").next_element.next_element.next_element.next_element.next_element
    # Get Very good Rating
    vOverallRatingContainer[1] = vSoupContainer.find(string = "Very good")
    vOverallRatingContainer[1] = vOverallRatingContainer[1].find_parent("div").next_element.next_element.next_element.next_element.next_element
    # Get Average Rating
    vOverallRatingContainer[2] = vSoupContainer.find(string = "Average")
    vOverallRatingContainer[2] = vOverallRatingContainer[2].find_parent("div").next_element.next_element.next_element.next_element.next_element
    # Get Poor Rating
    vOverallRatingContainer[3] = vSoupContainer.find(string = "Poor")
    vOverallRatingContainer[3] = vOverallRatingContainer[3].find_parent("div").next_element.next_element.next_element.next_element.next_element
    # Get Terrible Rating
    vOverallRatingContainer[4] = vSoupContainer.find(string = "Terrible")
    vOverallRatingContainer[4] = vOverallRatingContainer[4].find_parent("div").next_element.next_element.next_element.next_element.next_element
    # Total No Rating
    vOverallRatingContainer[5] = int(vOverallRatingContainer[0]) + int(vOverallRatingContainer[1]) + int(vOverallRatingContainer[2]) + int(vOverallRatingContainer[3]) + int(vOverallRatingContainer[4])
    
    vContainer.append(vOverallRatingContainer)
    entityId = vUrl.split("-")[2]
    entityName = vSoup.find('h1', {'id':'HEADING'}).text.strip()
    entity = {
        "entityId" : entityId,
        "name" : entityName,
        "rating" : {
            "excellent" : vOverallRatingContainer[0],
            "veryGood" : vOverallRatingContainer[1],
            "average" : vOverallRatingContainer[2],
            "poor" : vOverallRatingContainer[3],
            "terrible" : vOverallRatingContainer[4],
        }
    }
    dataManager.saveEntity(entity)
    #print(vContainer)  
    #--- Capture the User Names and User Profile Pages ---#
    vCount = 0
    pageNum = 1
    while True:
        # Save Output into CSV File
        if pageNum >= gStartPage-1:
            vCount = vCount + 1
            if vCount > gTotalPages:
                print ("********* REMOVE PAGE LIMIT *********** ")
                break
            # Creates a Parse-Tree
            vSoupLoops = BeautifulSoup(lSeleniumDriver.page_source, 'html.parser')
            #sleep(3)
            # vMemberContainer = fetchReviewerInfo(vSoupLoops)
            task = Task("PARSE_REVIEWERS", fetchReviewerInfo, fetchReviewerInfoCallback, vSoupLoops)
            gTaskMgr.addTaskQ(task)
            # vMainMemberContainer.append(vMemberContainer)
            # print("Display Name :", vMainMemberContainer[vMember][0], " - Username :", vMainMemberContainer[vMember][1], " - Member Profile :", vMainMemberContainer[vMember][2], " - Review Source :", vMainMemberContainer[vMember][3], " - Review Source URL :", vMemberContainer[4])
            vContainer.append(vMainMemberContainer)
            # f.close()
            print("Page ",vCount," of ",gTotalPages," completed extraction")
        else:
            print("Page ",pageNum," skipped extraction")
            # --- Get Next Button

        gNextButton = lSeleniumDriver.find_element_by_xpath("//*[@class='nav next taLnk ']")
        if gNextButton :
            gNextButton.click()
            sleep(1)
        else :
            break
        pageNum = pageNum + 1
    lSeleniumDriver.close()
    # return value
    return vContainer

def fetchReviewerInfo(htmlCode) :
    vMembers = htmlCode.findAll('div', {'class' : "memberOverlayLink"})
    vMembers = vMembers[::2]
    reviewListOut = []
    for vMember in vMembers:
        empty, uid, src = re.split('UID_|-|-SRC_', vMember['id'])
        # Get Display Name
        vDisplayName = vMember.find('div', class_='username')
        vDisplayName = vDisplayName.text.strip()
        vDisplayName = unicodedata.normalize('NFKD', vDisplayName).encode('ascii','ignore')
        vDisplayName = vDisplayName.decode("utf-8", "ignore")
        # Get the User Review Source
        vReviewSource = src.replace("SRC_","")
        vReviewSource = vReviewSource.replace(" ","")
        vDefaultReviewSourceURL = DEFAULT_REVIEW_SOURCE_URL
        vReviewSourceURL = vDefaultReviewSourceURL.replace("***", vReviewSource)
        # Get the URL of MembersOverlay for User
        vResponse = requests.get('http://www.tripadvisor.com.sg/MemberOverlay', params={'uid':uid})
        vOverlay = BeautifulSoup(vResponse.content, "html.parser")
        vUsername = vOverlay.find('a')['href']
        vUsername = vUsername.replace("/members/","")
        vMemberProfile = "https://www.tripadvisor.com.sg/members/" + vUsername
        
        reviewDistribution = vOverlay.findAll("span", {"class" : "rowCountReviewEnhancements rowCellReviewEnhancements"})
        
        #Build member dictionary
        memberData = {}
        memberData["displayName"] = vDisplayName
        memberData["userName"] = vUsername
        memberData["profileURL"] = vMemberProfile
        memberData["reviewID"] = vReviewSource
        memberData["reviewURL"] = vReviewSourceURL
        memberData["ratingDistribution"] = reviewDistribution
        reviewListOut.append(memberData)
    #print(reviewListOut)
    return reviewListOut
    

def fetchReviewerInfoCallback(futureObj) :
    log("@fetchReviewerInfoCallback", futureObj.result())
    profiles = futureObj.result()
    # Fetch the profile URL and scrap member details
    # Each profile will be queued for processing
    for profile in profiles :
        #persistReviewProfile(profile)
        profileUrl = profile['profileURL']
        print ("Processing MemberReview for", profile["userName"], profileUrl)
        payload= {}
        payload["profileUrl"] = profileUrl
        payload["ratingDistribution"] = profile["ratingDistribution"]
        task = Task("MEMBER_INFO", getMemberReviews, getMemberReviewsCallback, payload)
        gReviewerTaskMgr.addTaskQ(task)
    log("@fetchReviewerInfoCallback", "Done")


def fetchReviewers(targetURL, startPageNum, numPages) :  
    vYggdrasil = fMark_00(targetURL, startPageNum, numPages, 'div', 'id', 'taplc_location_detail_two_column_top_0')

def log(key, content):
    print(key, threading.currentThread().getName(), content)
    
def main(url, startPageNum, numPages):
    gReviewerTaskMgr = TaskManager("REVIEWER")
    fetchReviewers(url, startPageNum, numPages)
    #stopTask = Task("END_WORKER", None, None, None)
    #gTaskMgr.addTaskQ(stopTask)
    #gReviewTaskMgr.addTaskQ(stopTask)
    
if __name__ == '__main__':
    print (len(sys.argv))
    if (len(sys.argv) == 2) :
        main(sys.argv[1], 1, 20)
    elif (len(sys.argv) == 3) :
        main(sys.argv[1], int(sys.argv[2]), 20)
    elif (len(sys.argv) == 4) :
        main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        main(WEB_TARGET, 1, 20)
    #main(WEB_TARGET, 40, 1)   