SELECT 
    m.ID, 
    m.download_date, 
    m.series_id, 
    m.nzb_created, 
    m.description, 
    m.filename, 
    m.password, 
    m.note, 
    m.nzb_exception,
    m.movie_type,
    m.movie_url

FROM 
    movies m 
WHERE 
    (((m.nzb_created) Is Null) AND 
    ((m.description)<>"") AND 
    ((m.nzb_exception) Is Null))

ORDER BY 
    m.ID;