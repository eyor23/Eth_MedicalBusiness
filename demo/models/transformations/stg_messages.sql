-- models/transformation/stg_messages.sql
select 
        channel_title,
        channel_username,
        message_id,
        message,
        message_date,
        media_path,
        emoji_used,
        youtube_links 

from telegram_messages

