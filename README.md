# Air Quality Data

The goal of this project is to explore air quality data from different countries as a final project for the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main) offered by [DataTalks.Club](https://datatalks.club/).

# Data Sources

- Netherlands: https://statline.rivm.nl/portal.html?_la=en&_catalog=RIVM&tableId=50084NED&_theme=96

# Pre requisites

- Python 3.9
- Terraform
- Google Cloud Platform account
- Google Cloud CLI
- Docker

# Running

```sh
# set your GCP Project ID on environment variable
export GCP_PROJECT_ID="<YOUR GCP PROJECT ID GOES HERE>"

# login to gcp
gcloud init --project $GCP_PROJECT_ID

# deploy via terraform
cd terraform/data-platform
terraform init

export TF_VAR_gcp_project_id=$GCP_PROJECT_ID
terraform plan
terraform apply
```

# Running Prefect locally

```sh
# configure your settings
export PREFECT_POSTGRES_USER=prefect-db-user
export PREFECT_POSTGRES_PASSWORD=super-safe-password
export PREFECT_POSTGRES_DB=prefect_server
export GCP_GCS_DATA_LAKE_BUCKET_NAME=data-lake-$GCP_PROJECT_ID
export GCP_GCS_FLOWS_STORAGE_BUCKET_NAME=flows-storage-$GCP_PROJECT_ID

# install local requirements
source ./venv/Scripts/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# build prefect Docker images
docker build --no-cache -f ./prefect/PrefectServer.Dockerfile -t prefect-server:2.8.3 .
docker build --no-cache -f ./prefect/PrefectAgent.Dockerfile -t prefect-agent:2.8.3 .

# run infrastructure
docker-compose up
```

Deploying building blocks
```sh
# on VS Code
Tasks: Run Task > Prefect:Blocks:Run > gcp
Tasks: Run Task > Prefect:Flows:Deploy > health_check

# on terminal
python .\prefect\blocks\gcp.py
python .\prefect\flows\health_check\deployment.py
```

Access Prefect on browser https://localhost:4200.

# Cleaning up

```
cd terraform/data-platform
terraform destroy
```

# Architecture