CREATE TABLE movies_dev (
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
  PRIMARY KEY (ID)
  );