UPDATE 
    tbl_bulk_movie INNER JOIN movies m ON tbl_bulk_movie.movie_id = m.ID 

SET 
    m.description = "Vixen", 
    m.filename = [tbl_bulk_movie].[filename], 
    m.[password] = "<NONE>", 
    m.[note] = "Refer to movie_id 161; 2021";
