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
    IIF(
        (m.description Is Null) and 
        (m.filename is null) and
        (m.password is null) and
        (m.note is null) and
        (m.nzb_created is null) and
        (m.nzb_exception is null) and
        (m.dl_comments is null)        
        ,1,0) AS blank_flag

FROM 
    qry_movies_edit_main_filterx_tracking m;
