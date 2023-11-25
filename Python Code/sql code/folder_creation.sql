SELECT qry_movies_no_nzb.download_date, qry_movies_no_nzb.series_id, Count(qry_movies_no_nzb.ID) AS CountOfID
FROM qry_movies_no_nzb
GROUP BY qry_movies_no_nzb.download_date, qry_movies_no_nzb.series_id;
