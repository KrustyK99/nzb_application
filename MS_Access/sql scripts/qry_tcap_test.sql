SELECT 
    m.ID, 
    m.download_date, 
    m.series_id, 
    m.nzb_exception, 
    m.nzb_created, 
    m.filename, 
    m.password
FROM 
    movies m
WHERE 
    (((m.download_date)=#12/14/2023#) AND ((m.series_id)=3));
