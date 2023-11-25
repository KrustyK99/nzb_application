CREATE OR REPLACE vw_movies AS
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
    m.dl_comments 
FROM 
    movies m
WHERE
    (ID >= parameter_value(6)) AND 
    ((ID <= parameter_value(7)));
