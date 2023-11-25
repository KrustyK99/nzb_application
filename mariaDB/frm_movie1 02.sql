SELECT DISTINCT 
    m.series_id
FROM 
    movies_edit_main m
WHERE 
    m.download_date=[Forms]![movies1]![cbo_nzb_date];