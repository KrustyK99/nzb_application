CREATE OR REPLACE VIEW nzb_search AS
SELECT
    m.ID AS ID,
    m.download_date AS download_date,
    m.series_id AS series_id,
    m.description AS description,
    m.filename AS filename,
    m.password AS password,
    concat('https://www.nzbindex.nl/?q=', m.filename) AS nzb_address,
    concat(m.ID, ') ', '<a href=', '"https://www.nzbindex.nl/?q=', m.filename, '">', m.description, '</a>, ', m.filename, ', PW: ', m.password, '<br><br>') AS Link,
    m.nzb_exception AS nzb_exception,
    m.nzb_created
FROM
    movies m;