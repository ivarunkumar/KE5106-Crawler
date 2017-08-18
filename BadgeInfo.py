from Profile import Profile
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def fetchBadgeInfo(url):
    browser = webdriver.PhantomJS('phantomjs.exe')
    #browser.get('https://www.tripadvisor.com.sg/members/924dianae')
    browser.get(url)
    timeout = 1
    try:
        element_present = EC.presence_of_element_located((By.ID, 'element_id'))
        WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    html = browser.page_source
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    # find name
    profie = soup.find_all("span", {"class": "nameText "})
    Name = profie[0].get_text().strip()
    #print(Name)
    # find agesince
    ageSince = soup.find_all("div", {"class": "ageSince"})
    ASince = ""
    for since in ageSince:
        ASince += since.get_text().strip()
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
    #print(level)
    # find totalBadges
    totalBadges = soup.find_all("a", {"class": "totalBadges"})
    tBadges = totalBadges[0].get_text().strip()
    tBadgesLink = totalBadges[0]['href']
    #print(tBadges)
    #print(tBadgesLink)
    browser.get('https://www.tripadvisor.com.sg/' + tBadgesLink)
    html2 = browser.page_source
    soup2 = BeautifulSoup(html2, "html.parser")
    earnedBadges = soup2.find_all("li", {"class": "memberBadges"})
    #print(earnedBadges)
    Badges = []          ## Start as the empty list
    for Badge in earnedBadges:
        badgeText = Badge.find_all("div", {"class": "badgeText"})
        subText = Badge.find_all("span", {"class": "subText"})
        #print(badgeText[0].get_text().strip())
        # print(subText[0].get_text().strip())
        Badges.append(badgeText[0].get_text().strip()+","+subText[0].get_text().strip())
    p = Profile(Name,ASince,htown,points,level,tBadges,tBadgesLink,Badges)
    #print("----------------")
    #print(p.totalBadges)
    #myjson =json.dumps(p, default=lambda o: o.__dict__)
    #print (myjson)
    return p