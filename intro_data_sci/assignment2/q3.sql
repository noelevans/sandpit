-- select term, count from frequency where docid = '10080_txt_crude';
-- select term, count from frequency where docid = '17035_txt_earn';

-- For each of the queries above there was a number corresponding the 
-- term in the document. The similarity looks up to see if the same
-- term is in both documents. If it is the counts (occurence counts) are
-- multiplied together and the total sum is the answer


-- Final question
select docid, count from frequency where term = 'treasury';
