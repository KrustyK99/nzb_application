ALTER TABLE movies 
	ADD CONSTRAINT fk_movie_type_ID
	FOREIGN KEY(movie_type) REFERENCES movie_type(ID);
