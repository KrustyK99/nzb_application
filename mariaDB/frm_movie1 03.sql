SELECT TOP 1 
    m.ID, 
    m.download_date, 
    m.series_id
FROM 
    movies
WHERE 
    m.filename IS NULL AND 
    m.note IS NOT NULL
ORDER BY 
    m.ID;
