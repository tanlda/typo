select
    timestamp::date as date,
    count(*) as count
from
    {{ ref('stg_records') }}
where
    user_id = 'U000002'
    and timestamp >= now() - interval '60 days'
group by
    timestamp::date
order by
    date desc
