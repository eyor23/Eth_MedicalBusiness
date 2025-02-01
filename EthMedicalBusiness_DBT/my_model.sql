-- transform_data.sql
--with source_data as (
    select * from {{ ref('source_table') }}
--)

--select
    channel_title,
    channel_username, 
    message_id, 
    message, 
    message_date, 
    media_path, 
    emoji_used, 
    youtube_links
--from telegram_messages;

-- simple_model.sql
select * from telegram_messages;

