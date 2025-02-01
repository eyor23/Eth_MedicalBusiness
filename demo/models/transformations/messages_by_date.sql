-- models/transformations/messages_by_date.sql
with messages as (
    select * from {{ ref('stg_messages') }} -- Replace with your staging model name
)
select 
    channel_title,
    channel_username,
    message_id,
    message,
    message_date,
    media_path,
    emoji_used,
    youtube_links
from messages
where message_date between '2023-02-01 00:00:00' and '2023-02-02 23:59:59'
