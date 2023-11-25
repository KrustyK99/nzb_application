SELECT 
    z.ID, 
    z.download_date, 
    z.series_id, 
    z.description, 
    z.filename, 
    z.password, 
    z.nzb_address, 
    z.Link, 
    z.nzb_exception
FROM 
    nzb_search_dev.nzb_search z;

--    SELECT z.ID, z.download_date, z.series_id, z.description, z.filename, z.password, z.nzb_address, z.Link, z.nzb_exception FROM nzb_search_dev.nzb_search z;

