UPDATE 
    new_save_directories 
SET 
    download_date = REPLACE (SUBSTRING(download_date,3), '-','');