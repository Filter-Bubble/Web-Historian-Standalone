import os, sys, GenerateStandalone

databaseInputFile = os.path.join(os.path.expanduser("~"), "Library", "Safari", "History.db")
sqlHistoryItems = "\
	SELECT \
		history_items.id, \
		history_items.url, \
		history_visits.title, \
		MAX(CAST(1000 * history_visits.visit_time AS INT) + 978307200000) AS lastVisitTime, \
		history_items.visit_count AS visitCount, \
		0 AS typedCount \
	FROM history_visits \
	INNER JOIN history_items ON history_items.id = history_visits.history_item \
	GROUP BY history_items.id \
	ORDER BY history_visits.visit_time DESC;" # replace "typedCount" with real data if/when it becomes available in Safari
sqlVisitItems = "\
	SELECT \
		history_visits.history_item AS id, \
		history_visits.id AS visitId, \
		CAST(1000 * history_visits.visit_time AS INT) + 978307200000 AS visitTime, \
		IFNULL(history_visits.redirect_source, 0) AS referringVisitId, \
		CASE history_visits.redirect_source \
			WHEN NULL THEN \"typed\" \
			ELSE \"link\" \
		END AS transition, \
		history_visits.origin AS visitOrigin \
	FROM history_visits \
	ORDER BY history_visits.visit_time DESC;" # replace "transition" with real data if/when it becomes available in Safari

GenerateStandalone.generateStandalone(databaseInputFile, sqlHistoryItems, sqlVisitItems)