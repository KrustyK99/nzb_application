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
    m.movie_url, 
    m.filter_flag, 
    m.blank_flag
FROM 
    qry_movies_edit_main_filterx_tracking m
WHERE 
    m.download_date=#7/31/2022# AND 
    m.series_id=6 AND 
    m.nzb_created Is Null AND 
    m.nzb_exception Is Null;
