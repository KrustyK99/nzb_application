SELECT
    movies.ID, 
    movies.download_date,
    movies.description, 
    movies.dl_comments,
    movies.note, 
    movies.filename, 
    movies.password, 
    movies.series_id,
    movies.nzb_created, 
    movies.nzb_exception
FROM 
    movies
WHERE 
    movies.password Like "*MANY*";