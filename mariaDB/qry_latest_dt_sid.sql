SELECT TOP 1 
    m.ID, 
    m.download_date, 
    m.series_id
FROM 
    movies_edit_main m
WHERE 
    m.description IS NULL AND 
    m.note IS NULL
ORDER BY 
    m.ID;
