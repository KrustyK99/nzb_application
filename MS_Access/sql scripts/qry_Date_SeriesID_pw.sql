SELECT 
    m.ID, 
    m.filename, 
    m.password
FROM 
    tbl_Date_SeriesID INNER JOIN movies m
        ON (tbl_Date_SeriesID.series_id = m.series_id) AND (tbl_Date_SeriesID.dl_Date = m.download_date)
ORDER BY 
    m.ID;
