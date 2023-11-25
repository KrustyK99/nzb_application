-- This is the main data source for the form: movie1

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
    qry_movies_edit_main_filterx_tracking AS m

WHERE 
    ((m.download_date)=[Forms]![movies1]![cbo_nzb_date]) AND ((m.series_id)=[Forms]![movies1]![cbo_series_id]);