use TripAdvisor

db.Reviewers.createIndex({"userName" : 1}, {"unique":true})
db.Reviews.createIndex({"reviewId" : 1}, {"unique":true})
db.Reviews.createIndex({"reviewDate" : 1, "entityId" :1})
db.Reviews.createIndex({"reviewer" : 1})