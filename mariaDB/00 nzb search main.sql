CREATE TABLE movies (
    ID int NOT NULL AUTO_INCREMENT,
    download_date date,
    description varchar(1000) DEFAULT NULL,
    filename varchar(500) DEFAULT NULL,
    password varchar(500) DEFAULT NULL,
    series_id int(11) DEFAULT NULL,
    note longtext DEFAULT NULL,
    nzb_created int(11) DEFAULT NULL,
    nzb_exception int(11) DEFAULT NULL,
    dl_comments longtext DEFAULT NULL,
    movie_type int(11) DEFAULT NULL,
    movie_url varchar(250) DEFAULT NULL,
    PRIMARY KEY (ID)
    );
  
 CREATE TABLE movie_type (
    ID int(11) NOT NULL AUTO_INCREMENT,
    movie_type_name varchar(100) NOT NULL,
    movie_type_description varchar(250) DEFAULT NULL,
    PRIMARY KEY (ID)
    );
  
ALTER TABLE movies 
    ADD CONSTRAINT fk_movie_type_ID
    FOREIGN KEY(movie_type) REFERENCES movie_type(ID);