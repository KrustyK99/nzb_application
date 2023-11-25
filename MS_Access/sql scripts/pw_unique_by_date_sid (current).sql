SELECT DISTINCT 
    m.password

FROM 
    movies m

WHERE 
    (m.download_date=#3/1/2022# AND 
    m.password<>"<NONE>" AND 
    m.nzb_exception Is Null AND
        (m.series_id=7 OR 
        m.series_id=8 OR 
        m.series_id=8 ))

ORDER BY 
    m.password;
