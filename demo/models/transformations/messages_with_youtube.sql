-- models/transformations/messages_with_youtube.sql
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
where youtube_links is not null
