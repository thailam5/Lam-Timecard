from .postgres_conn import postgres_conn_tst

db = postgres_conn_tst()

def weeklyData():
    QUERY = """
WITH week_count AS (
SELECT
	date
	, EXTRACT('week' FROM date) AS week_no
	, clock_in 
	, clock_out
	, EXTRACT(epoch FROM (clock_out-clock_in))/3600 AS work_time
FROM daily_log dl
)
SELECT
	week_no
	,ROUND(14*SUM(work_time), 2) as "Pay"
FROM week_count
GROUP BY week_no
"""

    df = db.query(QUERY)

    return df