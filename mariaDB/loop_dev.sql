DELIMITER //

CREATE OR REPLACE PROCEDURE add_movie_blanks(
	IN dl_date varchar(20),
	IN sid int(11))

BEGIN

DECLARE i INT;

SET i = 1;

label1: LOOP

IF i <= 10 THEN
	INSERT INTO movies_dev (download_date, series_id) VALUES (STR_TO_DATE(dl_date , '%Y-%m-%d'), sid);
	SET i = i + 1;
	ITERATE label1;
END IF;
LEAVE label1;
END LOOP label1;

END; //

DELIMITER ;