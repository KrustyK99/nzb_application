-- Setup test data.
/* 
delete from movies_dev;
alter table movies_dev auto_increment = 1;
insert into movies_dev select * from movies where id>=376 and id<=584;
*/

-- Step 1: Add to 'comment' field the original 'filename'.
UPDATE movies_dev SET 
    note=CONCAT(note, char(13), char(10), "0131 Original Filename: ", filename)
WHERE 
    ID>=376 AND ID<=584;

