FROM jupyter/datascience-notebook

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates wget gcc build-essential libpq-dev && \
    apt-get clean

USER jovyan

RUN pip install polars pyarrow tqdm minio pyiceberg

RUN pip install sqlalchemy psycopg2

RUN pip install boto3

EXPOSE 8888

WORKDIR /home/jovyan/work

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''", "--no-browser"]
