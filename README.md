## Hello world!

# [#](https://microtypo.com/) Microtypo - Data Engineer Project
This is an end-to-end data engineer project to monitor my keystores, with the data flow is designed for maximizing automation and availability.

Related services are deployed on bare-metal [Kubernetes](https://kubernetes.io/), including most modern data tools and frameworks (OSS).

[Repositories](https://github.com/orgs/microtypo/repositories)

---

## Services

### [Typorio](https://github.com/microtypo/typorio)
- This is the python package that will be installed on one's machine
- It's job is to capture keystores and mouse clicks using [pynput](https://pypi.org/project/pynput/) and running as a [click](https://click.palletsprojects.com/) application
- After receiving 100 records (keystrokes), the timestamps of these records will be shuffled and then write as a .csv file under ~/microtypo/records/[timestamp].csv
- For an interval of 10 minutes (configurable), the above-mentioned .csv file is then uploaded on [Amazon S3](https://aws.amazon.com/s3/) using [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) with prefix such as records/2024-06/U000002/
- This process is to allow Typorio to upload records whenever internet connection is available, and leveraging S3's amazing [SLA](https://en.wikipedia.org/wiki/Service-level_agreement) attributes as the data lake to store raw .csv files.

### [Pipelines](https://github.com/microtypo/pipes)
- An implementation of [Dagster](https://dagster.io/) data pipelines orchestration, can be visited at: <https://dagster.microtypo.com/>
- A [Dagster Sensor](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) is set up to subscribe for new files arrive under a particular S3 Bucket (dev/stage/prod), with month-partitioned prefix to avoid hitting [list_objects_v2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html) api limitation (1,000 objects)  
- After a new s3 key is detected, a dagster runner is spin-up to download the file, shuffle all timestamps for all records (similar as above), and then:
    - Overwrite to a .parquet file stored in local [Minio](https://min.io/) storage with new records using [Polars](https://pola.rs/) with its awesome functionalities
    - Append new rows to the SQL data warehouse, implemented using [StackGres](https://stackgres.io/) with 2 nodes: primary and replication
- Additionally, a [Dagster Schedule](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) is set up to run [dbt](https://www.getdbt.com/) command for an interval of 1 hour ([cron expressions](https://crontab.guru/every-1-hour)), materializing defined models for data visualization using [Lightdash](https://www.lightdash.com/)

### [Dbt](https://github.com/microtypo/dbt)
- A minimal implementation of dbt, following this [structuring approach](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) with staging, intermediate and mart dbt models

### Others
- Kube: Kubernetes, Docker, Registry, Helm, Helmfile, Kubeadm, K9s
- Infra: S3, IAM, Cloudflare, Terraform, Terragrunt, Taskfile

---

[Demo](https://microtypo.com)
- [Dagster UI](https://dagster.microtypo.com/)
    - View-only
- [Apache Superset](https://dash.microtypo.com/) dashboard with prebuilt charts
    - username: admin
    - password: password
- [Lightdash](https://light.microtypo.com) dashboard for custom metrics
    - username: admin
    - password: password$
  
---

### Contact
- Email: <ledinhanhtan.stack@gmail.com>
- Social: <https://www.linkedin.com/in/tanlda/>
- GitHub: <https://github.com/tanlda>
