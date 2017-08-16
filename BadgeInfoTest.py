import fetchBadgeInfo from BadgeInfo
import profile
URLlist = ["https://www.tripadvisor.com.sg/members/924dianae", "https://www.tripadvisor.com.sg/members/iamKatyyAbdulla",
           "https://www.tripadvisor.com.sg/members/djc8888"]

for url in URLlist:
    p=fetchBadgeInfo(url=url)
    print(p.name)
    print(p.agesince)
    print(p.hometown)
    print(p.point)
    print(p.level)
    print(p.totalBadges)
    print(p.tBadgesLink)
    print(p.earnedBadges)
    print("===")


print("=THE END =")