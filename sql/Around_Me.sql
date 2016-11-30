/*
	 Around me member list 
*/

select
	mm.id as id 
	, mm.username as username 
	, ci.img_file as img_file 
   , string_agg(cch.tag_name, ', ') as tag_names 
	, mm.google_location as google_location 
from member_myuser mm 
left join 
( select 
	member_id, img_file 
	from collection_image where 
	img_order = 1 ) ci 
on ci.member_id = mm.id 
left join 
( select 
	chr.member_id, cht.tag_name 
	from collection_hash_relationship chr 
	join collection_hash_tag cht on cht.id = chr.hash_tag_id 
) cch 
on cch.member_id = mm.id 
group by 
mm.id, mm.username, ci.img_file, mm.created_date, mm.google_location 
order by 
mm.created_date 
DESC LIMIT 5;

			
			
			 
