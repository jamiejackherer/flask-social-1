SELECT *
FROM notification
WHERE payload_json
LIKE '%"post_id": 45%' AND '%"notifier_id": 6%';
