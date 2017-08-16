# ------- Import Library
import re
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from threading import Timer
from time import sleep
from TaskManager import TaskManager

import unicodedata

# ------- Website to Crawl
#gWebTarget = "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d2139448-Reviews-ION_Orchard-Singapore.html"
WEB_TARGET = "https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-Reviews-Universal_Studios_Singapore-Sentosa_Island.html"
DEFAULT_REVIEW_SOURCE_URL = "https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-r***-Universal_Studios_Singapore-Sentosa_Island.html#REVIEWS"
# ------- Selanium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#gSeleniumDriver = webdriver.Chrome(executable_path=r"E:\chromedriver_win32\chromedriver.exe")
gSeleniumDriver = webdriver.Chrome()

#assert "ION" in gSeleniumDriver.title
# Global Set-up
#gClient = MongoClient("localhost", 27017)
#gDb = gClient.OrchandIon
#gCollection = gDb.Init

# ------- Set Global Variables
gYggdrasil = [] #--- Array container for Parse-Trees

gTaskMgr = TaskManager()
# ------- Function Calls
# HTML Convert to Parse-Tree Search Mark-00
def fMark_00(vUrl, vParameter1, vParameter2a, vParameter2b) :
  lSeleniumDriver = webdriver.Chrome()
  
  # ------- Total Number of Pages
  gStartPage = 0
  gTotalPages = 200 # 1176 48 pages
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
  print(vContainer)  
  #--- Capture the User Names and User Profile Pages ---#
  vCount = 0
  
  for i in range(gTotalPages):
    vCount = vCount + 1
    # Save Output into CSV File
    if i >= gStartPage-1:
        # Lets skip writing to file
        # if gStartPage == 1 and i == 0:
        #     f = open('E:/Temp/USS_Reviewers.csv', 'w', newline="\n") # open a csv file for writing
        #     f.write("Page" + ',' + "Display Name" + ',' + "Username" + ',' + "Member Profile" + ',' + "Review Source" + ',' + "Review Source URL" + "\n")
        # else:
        #     f = open('E:/Temp/USS_Reviewers.csv', 'a', newline="\n") # open a csv file for append
         
        # Creates a Parse-Tree
        vSoupLoops = BeautifulSoup(lSeleniumDriver.page_source, 'html.parser')
        #sleep(3)
        # vMemberContainer = fetchReviewerInfo(vSoupLoops)
        gTaskMgr.addTask(fetchReviewerInfo, fetchReviewerInfoCallback, vSoupLoops)
        # vMainMemberContainer.append(vMemberContainer)
        # print("Display Name :", vMainMemberContainer[vMember][0], " - Username :", vMainMemberContainer[vMember][1], " - Member Profile :", vMainMemberContainer[vMember][2], " - Review Source :", vMainMemberContainer[vMember][3], " - Review Source URL :", vMemberContainer[4])
        vContainer.append(vMainMemberContainer)
        # f.close()
        print("Page ",vCount," of ",gTotalPages," completed extraction")
    else:
        print("Page ",vCount," of ",gTotalPages," skipped extraction")
        # --- Get Next Button
    if vCount < gTotalPages:
                    gNextButton = lSeleniumDriver.find_element_by_xpath("//*[@class='nav next taLnk ']")
                    gNextButton.click()
                    
    sleep(1)
    
  lSeleniumDriver.close()
  # return value
  return vContainer

def fetchReviewerInfo(htmlCode) :
    vMembers = []
    vMemberContainer = []
    vMembers = htmlCode.findAll('div', {'class' : "memberOverlayLink"})
    vMembers = vMembers[::2]
    reviewListOut = []
    for vMember in vMembers:
        empty, uid, src = re.split('UID_|-|-SRC_', vMember['id'])
        vMemberContainer = ["","","","",""]
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
        
        #Build member dictionary
        memberData = {}
        memberData["displayName"] = vDisplayName
        memberData["userName"] = vUsername
        memberData["profileURL"] = vMemberProfile
        memberData["reviewID"] = vReviewSource
        memberData["reviewURL"] = vReviewSourceURL
        reviewListOut.append(memberData)
    #print(reviewListOut)
    return reviewListOut
    

def fetchReviewerInfoCallback(ftr) :
    print("@callback", ftr.result())

def fetchReviewers(targetURL) :  
    vYggdrasil = fMark_00(targetURL, 'div', 'id', 'taplc_location_detail_two_column_top_0')

# Save Output into CSV File
#f = open('E:/Temp/USS_Reviewers.csv', 'w', newline="\n") # open a csv file for writing

# --- Write CSV headers
# --- Find Total Rating Count
#vTotalRatingsInvYggdrasil = len(vYggdrasil[0])
#f.write("Excellent" + ',' + "Very good" + ',' + "Average" + ',' + "Poor" + ',' + "Terrible" + ',' + "Total No Rating" + "\n")
#f.write(str(vYggdrasil[0][0]) + ',' + str(vYggdrasil[0][1]) + ',' + str(vYggdrasil[0][2]) + ',' + str(vYggdrasil[0][3]) + ',' + str(vYggdrasil[0][4]) + ',' + str(vYggdrasil[0][5]) + "\n")

#vDocument = {'Excellent':vYggdrasil[0][0],
#                'Very good':vYggdrasil[0][1],
#       'Average':vYggdrasil[0][2],
#       'Poor':vYggdrasil[0][3],
#       'Terrible':vYggdrasil[0][4],
#       'Total No Rating':vYggdrasil[0][5]}
#gCollection.insert(vDocument)

  
# --- Write CSV headers
# --- Find Total Member Count
#vTotalMembersInvYggdrasil = len(vYggdrasil[1])
#f.write("Display Name" + ',' + "Username" + ',' + "Member Profile" + ',' + "Review Source" + ',' + "Review Source URL" + "\n")

# --- Run a Loop -> Write Each Row into CSV
#for i in range(vTotalMembersInvYggdrasil):
# f.write(vYggdrasil[1][i][0] + ',' + vYggdrasil[1][i][1] + ',' + vYggdrasil[1][i][2] + ',' + vYggdrasil[1][i][3] + ',' + vYggdrasil[1][i][4] + "\n")
  #vDocument = {'Display Name':vYggdrasil[1][i][0],
  #       'Username':vYggdrasil[1][i][1],
  #       'Member Profile':vYggdrasil[1][i][2],
  #       'Review Source':vYggdrasil[1][i][3],
  #       'Review Source URL':vYggdrasil[1][i][4]}
  #gCollection.insert(vDocument)
    
#f.close() # close the file

#print("Number of Documents Inserted :", gCollection.count())

#for x in gCollection.find():
# print(x)

#gClient.close() # close mongoDB
