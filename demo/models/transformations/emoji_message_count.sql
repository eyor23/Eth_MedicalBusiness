-- models/transformations/emoji_message_count.sql

with messages as (
    select 
        *,
        case 
            when emoji_used = 'true' then true
            when emoji_used = 'false' then false
            else null -- Set to null for non-boolean values
        end as emoji_used_boolean
    from {{ ref('stg_messages') }}
)

select 
    count(*) as emoji_message_count
from messages
where emoji_used_boolean = true