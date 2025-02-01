-- models/transformations/group_messages_by_channel.sql
with messages as (
    select * from {{ ref('stg_messages') }} -- Replace with your staging model name
)
select 
    channel_title,
    count(*) as message_count
from messages
group by channel_title
