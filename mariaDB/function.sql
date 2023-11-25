CREATE or replace FUNCTION FortyTwo() RETURNS tinyint(4)
    DETERMINISTIC
BEGIN
 DECLARE x TINYINT;
    set x = select series_id from movies where id = 10;
 RETURN x;
END



CREATE or replace FUNCTION lower_bound (movie_id TINYTEXT) RETURNS INT RETURN
  (SELECT MAX(series_id) FROM movies WHERE id = movie_id);
