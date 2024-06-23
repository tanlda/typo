select count(*) from {{ ref('stg_records') }}
