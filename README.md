# KE5106-Crawler
A Spider for KE5106 Continuous Assessment

# Prerequisties
1. Python 3.5 or greater
2. MongoDB 3.4
3. Python Modules
	* chromedriver_installer
	* selenium
	* virtualenv
	* requests
	* flask
	* flask-jsonpify
	* flask-restful
	* pymongo
	* sklearn
	* numpy
	* scipy
	* numpy+mkl


# Crawler Usage Steps
## Running the Crawler
Will crawl and attraction and persist the scrapped data into mongo

cd to the folder containing the code.
python FetchReviewers.py <TripAdvisor Attraction Home URL> <Start Page> <Number of Pages>
Example : 
python FetchReviewers.py https://www.tripadvisor.com.sg/Attraction_Review-g294265-d1438273-Reviews-Buddha_Tooth_Relic_Temple_and_Museum-Singapore.html 1 2

## Import Existing Data
1. run resources/DbSetup.js
2. cd to dbdump folder
3. run the script within resources/db-import.txt

## Data Preparation - Manual step
run script resources/DataPreProcessing.js

# API Usage
1. run python api.py

## API for Reviewer Rating
http://127.0.0.1:5000/review/{reviewerId} where {reviewerId} is the user's profile id. 
example: http://127.0.0.1:5000/review/MisterGong

## API for Entities Rating
http://127.0.0.1:5000/entity/{entityId} where {entity} is the attraction id. 
example: http://127.0.0.1:5000/entity/d2439664
