FROM prefecthq/prefect:2.8.3-python3.9

RUN apt update && \
    pip install psycopg2-binary \
                prefect-gcp[cloud_storage]==0.3.0 \
                gcsfs==2023.1.0