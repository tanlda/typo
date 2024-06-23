CREATE
EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE records
(
    user_id   VARCHAR,
    type      VARCHAR(2),
    key       VARCHAR(144),
    meta      JSONB,
    hostname  TEXT,
    timestamp TIMESTAMPTZ
);
SELECT create_hypertable('records', by_range('timestamp'));

CREATE INDEX user_idx ON public.records (user_id);
CREATE INDEX key_idx ON public.records (key);
CREATE INDEX type_idx ON public.records (type);
