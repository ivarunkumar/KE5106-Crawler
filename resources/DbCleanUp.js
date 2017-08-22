use TripAdvisor
cleanup = function () {
	db.Reviews.remove({});
	db.Reviewers.remove({});
	db.Entities.remove({});
}

cleanup();