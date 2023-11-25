-- Step 1: Concatenate un-encoded filename to description.
-- UPDATE movies SET description=concat(description, ' - ', filename) WHERE ID>=826 and ID<=830;

-- Step 2: Add comment to Notes Section

-- Testing for NULL and providing a value
SELECT 
    filename, 
    if(IFNULL(filename,'0')='0',description,CONCAT() (description,' - ',filename)) AS NEW_Description 
FROM
    movies 
WHERE 
    id>=826 AND id<=830;