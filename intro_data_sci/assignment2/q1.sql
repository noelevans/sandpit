-- reuters: frequency(docid, term, count)

--select * from frequency limit 5;

select count(*) from frequency where docid = '10398_txt_earn';

select count(term) 
from frequency 
where docid = '10398_txt_earn' and count = 1;

select distinct count(term) from (
    select term 
    from frequency 
    where docid = '10398_txt_earn' and count = 1 
        union
    select term 
    from frequency 
    where docid = '925_txt_trade' and count = 1
);

select count(docid) from frequency where term = 'parliament';

select count(*) 
from   (select docid 
        from frequency group by docid having sum(count) > 300);

select count(*) 
from frequency f 
join frequency g on f.docid == g.docid 
where f.term = 'transactions' and g.term = 'world';
