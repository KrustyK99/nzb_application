SELECT 
    m.ID, 
    m.download_date, 
    m.description, 
    m.filename, 
    m.password, 
    m.series_id, 
    m.note, 
    m.nzb_created, 
    m.nzb_exception, 
    m.dl_comments, 
    m.movie_type, 
    m.movie_url
FROM 
    movies m
WHERE 
    ((m.download_date='2022-10-12') AND 
    (m.series_id=7) AND 
    (m.nzb_created Is Null) AND 
    (m.nzb_exception Is Null));
