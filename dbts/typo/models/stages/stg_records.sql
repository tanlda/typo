with formatted as (
    select
        user_id,
        type,
        key,
        meta::text as meta,
        timestamp
    from {{ source('typo', 'records') }}
)
select * from formatted
