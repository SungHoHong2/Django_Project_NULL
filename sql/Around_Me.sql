/*
	 Around me member list 
*/

select
	mm.id as id 
	, mm.username as username 
	, ci.img_file as img_file 
    , cch.tag_names as tag_names  
	, mm.google_location as google_location 
	, mlr.likes as likes 
from member_myuser mm 
left join 
( select 
	member_id, img_file 
	from collection_image where 
	img_order = 1 ) ci 
on ci.member_id = mm.id 
left join 
( select 
	chr.member_id, string_agg(cht.tag_name, ', ') as tag_names 
	from collection_hash_relationship chr 
	join collection_hash_tag cht on cht.id = chr.hash_tag_id 
	group by chr.member_id  
) cch 
on cch.member_id = mm.id 
left join (  
  select mlr.followee_id, count(id) as likes from 
  member_like_relationship mlr 
  group by mlr.followee_id
) mlr on mlr.followee_id = mm.id
order by 
mm.created_date 
DESC LIMIT 5 OFFSET 1;


select * from member_like_relationship;
			
			
delete from member_like_relationship;
			 
