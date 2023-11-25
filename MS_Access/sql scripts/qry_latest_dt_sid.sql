SELECT TOP 1 
    m.ID, 
    m.download_date, 
    m.series_id

FROM 
    movies_edit_main AS m

WHERE 
    m.description IS NULL AND 
    m.note IS NULL AND
    m.nzb_exception IS NULL
ORDER BY 
    m.ID;
