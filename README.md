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
# login to gcp
gcloud init

# deploy the data platform
cd terraform/data-platform
terraform init
terraform plan -var 'project=<YOUR GCP PROJECT ID>'
```

# Running Prefect locally

```sh
source ./venv/Scripts/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

docker build --no-cache -f Dockerfile -t prefect-orion:2.8.3 .
docker-compose up
```

Access Prefect on browser https://localhost:4200.

# Cleaning up

```
cd terraform/data-platform
terraform destroy
```

# Architecture