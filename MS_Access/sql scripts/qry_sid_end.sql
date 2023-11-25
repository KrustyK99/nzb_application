SELECT DISTINCT TOP 1 
    m.series_id

FROM 
    qry_movies_edit_main_filterx_tracking m

WHERE 
    m.blank_flag=1

ORDER BY 
    m.series_id DESC;