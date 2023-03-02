FROM prefecthq/prefect:2.8.3-python3.9

RUN apt update && \
    pip install psycopg2-binary