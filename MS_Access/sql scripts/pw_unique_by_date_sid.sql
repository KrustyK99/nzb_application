SELECT DISTINCT 
    m.password

FROM 
    movies m

WHERE 
    (m.download_date=#2/8/2022# AND 
    m.password<>"<NONE>" AND 
        (m.series_id=5 OR 
        m.series_id=6 OR 
        m.series_id=7 OR 
        m.series_id=8 OR 
        m.series_id=9 OR 
        m.series_id=10))

ORDER BY 
    m.password;
