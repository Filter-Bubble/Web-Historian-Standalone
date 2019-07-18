import os, GenerateStandalone

databaseInputFile = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Google", "Chrome", "Default", "History")
sqlHistoryItems = "\
	SELECT \
		urls.id, \
		urls.url, \
		urls.title, \
		CAST(urls.last_visit_time / 1000 AS INT) - 11644473600000 AS lastVisitTime, \
		urls.visit_count AS visitCount, \
		urls.typed_count AS typedCount \
	FROM urls \
	ORDER BY lastVisitTime DESC;"
sqlVisitItems = "\
	SELECT \
		visits.url AS id, \
		visits.id AS visitId, \
		CAST(visits.visit_time / 1000 AS INT) - 11644473600000 AS visitTime, \
		visits.from_visit AS referringVisitId, \
		CASE (16 + visits.transition % 16) % 16 \
			WHEN 0 THEN \"link\" \
			WHEN 1 THEN \"typed\" \
			WHEN 2 THEN \"auto_bookmark\" \
			WHEN 3 THEN \"auto_subframe\" \
			WHEN 4 THEN \"manual_subframe\" \
			WHEN 5 THEN \"generated\" \
			WHEN 6 THEN \"auto_toplevel\" \
			WHEN 7 THEN \"form_submit\" \
			WHEN 8 THEN \"reload\" \
			WHEN 9 THEN \"keyword\" \
			WHEN 10 THEN \"keyword_generated\" \
			ELSE \"typed\" \
		END AS transition, \
		IFNULL(visit_source.source, 999) AS visitOrigin \
	FROM visits \
	LEFT JOIN visit_source on visits.id = visit_source.id \
	ORDER BY visits.visit_time DESC;"

GenerateStandalone.generateStandalone(databaseInputFile, sqlHistoryItems, sqlVisitItems)