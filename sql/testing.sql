SELECT notified.username, notifier.username, notifier.active
FROM notification_post
JOIN user AS notified ON notified.id = notified_id
JOIN user AS notifier ON notifier.id = notifier_id
WHERE notifier.active = 1;
