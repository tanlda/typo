with source as (
    select
        user_id,
        occupation,
        num_keyboards,
        created_at,
        updated_at,
        deleted_at
    from {{ source('typo', 'users') }}
)
select * from source
