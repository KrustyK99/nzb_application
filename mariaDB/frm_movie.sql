SELECT 
    m.ID, 
    m.download_date, 
    m.description, 
    m.filename, 
    m.password, 
    m.series_id, 
    m.note
FROM 
    movies m
WHERE 
    m.download_date=[Forms]![movies]![cbo_nzb_date] AND 
    m.series_id=[Forms]![movies]![cbo_series_id];
