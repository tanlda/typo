FROM python:3.10-slim

ENV DAGSTER_HOME=/opt/dagster/dagster_home
ENV DAGSTER_APP=/opt/dagster/app

RUN mkdir -p $DAGSTER_HOME $DAGSTER_APP

WORKDIR $DAGSTER_APP

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates wget gcc build-essential libpq-dev && \
    apt-get clean

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN pip install dbt-core dbt-postgres

COPY ./typo ./typo

COPY ./data ./data

COPY ./dbt ./dbt

RUN dbt deps --project-dir ./dbt --profiles-dir ./dbt && \
    dbt parse --project-dir ./dbt --profiles-dir ./dbt

EXPOSE 4000

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "typo"]
