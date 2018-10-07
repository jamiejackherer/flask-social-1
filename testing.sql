SELECT *, NULL AS comment_id
FROM post_notification AS pn
WHERE pn.notified_id = 1
UNION ALL
SELECT *
FROM comment_notification AS cn
WHERE cn.notified_id = 1;
