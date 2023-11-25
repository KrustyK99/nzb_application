-- CREATE OR REPLACE VIEW movies_edit_main AS

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
    (m.ID >= parameter_value(6)) AND 
    (m.ID <= parameter_value(7)) AND
    (m.download_date >= parameter_value(8)) AND
    (m.download_date <= parameter_value(9))
ORDER BY
	ID ASC;