-- Create Aggr with Output
db.Reviews.aggregate([
{"$group":
	{
		"_id": "$reviewerId", 
		"num_reviews" : {$sum : 1},
		"num_helpful": {"$sum": {$cond:[{"$gte":["$helpfulVote",1]}, 1, 0]}},
		"Rating_1": {"$sum": {"$cond": [ { "$eq": [ "$rating", 1 ] }, 1, 0 ]}},
		"Rating_2": {"$sum": {"$cond": [ { "$eq": [ "$rating", 2 ] }, 1, 0 ]}},
		"Rating_3": {"$sum": {"$cond": [ { "$eq": [ "$rating", 3 ] }, 1, 0 ]}},
		"Rating_4": {"$sum": {"$cond": [ { "$eq": [ "$rating", 4 ] }, 1, 0 ]}},
		"Rating_5": {"$sum": {"$cond": [ { "$eq": [ "$rating", 5 ] }, 1, 0 ]}},
		"Cat_AttractiveReview_Ind": {"$sum": {$cond:[{"$eq":["$category","Attraction_Review"]}, 1, 0]}},
		"Cat_RestaurantReview_Ind": {"$sum": {$cond:[{"$eq":["$category","Restaurant_Review"]}, 1, 0]}},
		"Cat_HotelReview_Ind": {"$sum": {$cond:[{"$eq":["$category","Hotel_Review"]}, 1, 0]}},
		"Cat_AirlineReview_Ind": {"$sum": {$cond:[{"$eq":["$category","Airline_Review"]}, 1, 0]}},
		"Cat_NULL_Ind": {"$sum": {$cond:[{"$eq":["$category","NULL"]}, 1, 0]}},
		"SS_Pos_Ind": {"$sum": {$cond:[{"$eq":["$sentimentScore.label","pos"]}, 1, 0]}},
		"SS_Neg_Ind": {"$sum": {$cond:[{"$eq":["$sentimentScore.label","neg"]}, 1, 0]}},
		"SS_Neutral_Ind": {"$sum": {$cond:[{"$eq":["$sentimentScore.label","neutral"]}, 1, 0]}},
		"SS_NA_Ind": {"$sum": {$cond:[{"$eq":["$sentimentScore.label","NA"]}, 1, 0]}}
	}
},
{$out:"ReviewsAggr"}])

db.Reviewers.aggregate([
{$unwind: '$travelStyle'},
{"$group":
	{
		"_id": "$userName",
		"TS_ArtAndArchitecture_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Art and Architecture Lover"]}, 1, 0]}},
		"TS_Foodie_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Foodie"]}, 1, 0]}}, 
		"TS_HistoryBuff_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","History Buff"]}, 1, 0]}},
		"TS_Nature_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Nature Lover"]}, 1, 0]}},
		"TS_UrbanExplorer_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Urban Explorer"]}, 1, 0]}},
		"TS_Backpacker_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Backpacker"]}, 1, 0]}},
		"TS_BeachGoer_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Beach Goer"]}, 1, 0]}},
		"TS_Ecotourist_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Eco-tourist"]}, 1, 0]}},
		"TS_LikeALocal_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Like a Local"]}, 1, 0]}},
		"TS_PeaceQuietSeeker_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Peace and Quiet Seeker"]}, 1, 0]}},
		"TS_Thrifty Traveller_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Thrifty Traveller"]}, 1, 0]}},
		"TS_ThrillSeeker_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Thrill Seeker"]}, 1, 0]}},
		"TS_Trendsetter_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Trendsetter"]}, 1, 0]}},
		"TS_FamilyHolidayMaker_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Family Holiday Maker"]}, 1, 0]}},
		"TS_LuxuryTraveller_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Luxury Traveller"]}, 1, 0]}},
		"TS_NightlifeSeeker_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Nightlife Seeker"]}, 1, 0]}},
		"TS_Vegetarian_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Vegetarian"]}, 1, 0]}},
		"TS_ShoppingFanatic_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","Shopping Fanatic"]}, 1, 0]}},
		"TS_60PlusTraveller_Ind": {"$sum": {$cond:[{"$eq":["$travelStyle","60+ Traveller"]}, 1, 0]}}
	}
},
{$out:"ReviewersTransform"}])