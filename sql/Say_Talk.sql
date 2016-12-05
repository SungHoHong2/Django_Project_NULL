

/*
  TalkDetailPageView
  main_post
*/


SELECT ss.id,
       ci.img_file         AS profile_img,
       postimg.talk_images AS talk_images,
       ss.content          AS content,
       ss.title            AS title,
       chrs.tag_names      AS tag_names
  FROM saytalk_saytalk ss
       JOIN member_myuser mm
          ON ss.created_by != '' AND mm.id = ss.created_by::Integer
       JOIN collection_image ci ON ci.member_id = mm.id AND ci.img_order = 1
       JOIN
       (  SELECT ci2.say_talk_id,
                 string_agg (ci2.img_file, ', ') AS talk_images
            FROM collection_image ci2
           WHERE ci2.say_talk_id = 32
        GROUP BY ci2.say_talk_id) postimg
          ON postimg.say_talk_id = ss.id
       JOIN
       (  SELECT chr.say_talk_id, string_agg (c.tag_name, ', ') AS tag_names
            FROM collection_hash_relationship chr
                 JOIN collection_hash_tag c ON c.id = chr.hash_tag_id
           WHERE chr.say_talk_id = 32
        GROUP BY say_talk_id) chrs
          ON chrs.say_talk_id = ss.id
 WHERE ss.id = 32;
 
 
/*
  TalkDetailPageView
  sub_posts
*/
 
 select 
       ss.id,
       ci.img_file         AS profile_img,
       postimg.talk_images AS talk_images,
       ss.content          AS content,
       ss.title            AS title
   FROM saytalk_talk_relationship sr
       JOIN saytalk_saytalk ss on sr.followee_id=36 and ss.id = sr.follower_id 	  
	   JOIN member_myuser mm
          ON ss.created_by != '' AND mm.id = ss.created_by::Integer
       JOIN collection_image ci ON ci.member_id = mm.id AND ci.img_order = 1
       LEFT JOIN
       (  SELECT ci2.say_talk_id,
                 string_agg (ci2.img_file, ', ') AS talk_images
            FROM collection_image ci2
        GROUP BY ci2.say_talk_id) postimg
          ON postimg.say_talk_id = sr.follower_id	 ;
		  
		