FROM prefecthq/prefect:2.8.3-python3.9

RUN apt update && \
    python -m pip install --upgrade pip

# installing the packages from copied files so we can handle authentication
# for private python repository out of Dockerfile
COPY ./__pypackages__/ /__pypackages__/
RUN pip install --no-index --find-links=/__pypackages__/ /__pypackages__/*
