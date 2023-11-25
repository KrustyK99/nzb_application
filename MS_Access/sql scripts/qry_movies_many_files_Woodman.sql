SELECT 
    m.ID, 
    m.download_date, 
    m.description, 
    m.dl_comments, 
    m.note, 
    m.filename, 
    m.password, 
    m.series_id, 
    m.nzb_created, 
    m.nzb_exception, 
    m.movie_url
FROM 
    movies m
WHERE 
    m.description Like "*woodman*" AND 
    m.password Like "*MANY*" AND
    m.nzb_created Is Null

ORDER BY 
    m.ID;