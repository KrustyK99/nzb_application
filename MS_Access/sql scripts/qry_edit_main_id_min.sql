SELECT TOP 1 
    m.ID

FROM qry_movies_edit_main_filterx_tracking m

WHERE m.blank_flag=1

ORDER BY 
    m.ID;
