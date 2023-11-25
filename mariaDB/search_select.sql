DELIMITER $$

CREATE PROCEDURE find_movie_by_filename(
	IN string_frag varchar(100)
	)

BEGIN

-- SET @search_string = '%sZUgq19b3%';

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
	movies AS m
WHERE 
	(m.filename LIKE string_frag) OR
	(m.description LIKE string_frag) OR
	(m.password LIKE string_frag) OR
	(m.note LIKE string_frag)
ORDER BY 
	m.ID;

END$$

DELIMITER;