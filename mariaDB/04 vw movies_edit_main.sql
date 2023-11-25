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
    m.dl_comments,
    m.movie_type,
    m.movie_url

FROM 
    movies m

WHERE
    (m.ID >= parameter_value(6)) AND 
    (m.ID <= parameter_value(7))
    
ORDER BY
	m.ID ASC;