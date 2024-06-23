with broadcast as (
    select
        count(*) as total
    from
        {{ ref('stg_records') }}
),
summary as (
    select
        u.occupation,
        r.key,
        count(*) as group_count,
        (select count(distinct occupation) from {{ ref('stg_users') }}) as num_occupations
    from
        {{ ref('stg_users') }} u
    join
        {{ ref('stg_records') }} r on u.user_id = r.user_id
    group by
        u.occupation, r.key
)
select
    s.occupation,
    s.key,
    s.group_count as count,
    round(100.0 * s.group_count / b.total, 2) as percentage,
    round(1.0 * s.group_count / coalesce(num_occupations, 1)) as average
from
    summary s
cross join
    broadcast b
order by
    average desc
limit
    20
