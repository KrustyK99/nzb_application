SELECT *
    FROM (
        
SELECT 
    m.ID, 
    m.download_date, 
    m.description, 
    m.filename, 
    m.password, 
    m.series_id, 
    m.note, 
    m.nzb_created, 
    m.nzb_exception, 
    m.dl_comments, 
    m.movie_type, 
    m.movie_url, 
    IIf(Nz([movie_type])=0,1, 
        IIf(Nz([movie_type])=4,0, 
            IIf(Nz([movie_type])>0,1,0))) AS filter_flag, 
    IIf(
        (m.description Is Null) And 
        (m.filename Is Null) And 
        (m.password Is Null) And 
        (m.note Is Null) And 
        (m.nzb_created Is Null) And 
        (m.nzb_exception Is Null) And 
        (m.dl_comments Is Null), 1,0) AS blank_flag 
FROM 
    movies_edit_main AS m)  AS m1

WHERE 
    (((m1.filter_flag)=1));