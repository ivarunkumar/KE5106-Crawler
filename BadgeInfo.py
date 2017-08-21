from Profile import Profile
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def fetchBadgeInfo(soup):
    #browser = webdriver.PhantomJS('phantomjs.exe')
    # find name
    profileTmp = soup.find_all("span", {"class": "nameText "})
    Name = profileTmp[0].get_text().strip()
    #print(Name)
    # find agesince
    ageSince = soup.find_all("div", {"class": "ageSince"})
    ageSince2 =ageSince[0].find_all("p")
    ASince = ageSince2[0].get_text().strip()
    ASince = ASince[-4:]
    Age = ''
    sex=''

    try:
        Age = ageSince2[1].get_text().strip()
        Age=Age.lower()


        if "female" in Age:
            sex = 'female'
            Age = Age.replace('female', '')
            Age = Age.replace('year old', '')


        if "male" in Age:
            sex='male'
            Age =Age.replace('male', '')
            Age = Age.replace('year old', '')

    except:
        Age = ''

#  for since in ageSince:
     #   ASince += since.get_text().strip()

    #print(ASince)

    # find hometown
    hometown = soup.find_all("div", {"class": "hometown"})

    htown = ""

    for home in hometown:
        htown += home.get_text().strip()

    #print(htown)

    # find total point
    points = soup.find_all("div", {"class": "points"})
    points = points[0].get_text().strip()

    #print(points)

    # find level
    tripcollectiveinfo = soup.find_all("div", {"class": "level tripcollectiveinfo"})
    # print(tripcollectiveinfo)
    level = tripcollectiveinfo[0].get_text().strip()
    level = level.replace('Level', '')
    level = level.replace('Contributor', '')

    #print(level)

    # find totalBadges
    totalBadges = soup.find_all("a", {"class": "totalBadges"})
    tBadges = totalBadges[0].get_text().strip()
    tBadges=tBadges.replace('total', '')
    tBadgesLink = totalBadges[0]['href']

    #print(tBadges)
    #print(tBadgesLink)

    tagBlocklist = []
#    tagBlock = soup.find_all("div", {"class": "memberTags"})
    tagBlock = soup.find_all("div", {"class": "tagBubble unclickable"})
    for tag in tagBlock:
        #print(tag.get_text().strip())
        tagBlocklist.append(tag.get_text().strip())

    Largebadge= []
    LargebadgeSoup =soup.find_all("div", {"class": "badgeList badgeListLoggedOut"})

    for tagbadge in LargebadgeSoup:

        Largebadgename = tagbadge.find_all("div", {"class": "badgeName"})
        LargebadgeText = tagbadge.find_all("div", {"class": "badgeSubtext"})

        for i in range(0, len(Largebadgename)):
            Largebadge.append(Largebadgename[i].get_text().strip()+": "+LargebadgeText[i].get_text().strip() )


        print (Largebadgename)

    p = Profile(Name,ASince,Age,sex,htown,points,level,tagBlocklist,Largebadge,tBadges,tBadgesLink)
    return p

def fetchBadgeInfoCallback(futureObj):
    print("@fetchBadgeInfoCallback", futureObj.result())