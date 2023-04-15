resource "google_service_account" "spark_agent_service_account" {
  account_id   = "sa-spark-agent"
  display_name = "Spark Agent Service Account"
}

resource "google_project_iam_member" "spark_agent_service_account_dataproc_worker" {
  project = var.gcp_project_id
  role    = "roles/dataproc.worker"
  member  = google_service_account.spark_agent_service_account.member
}

resource "google_project_iam_member" "spark_agent_service_account_bigquery_job_user" {
  project = var.gcp_project_id
  role    = "roles/bigquery.jobUser"
  member  = google_service_account.spark_agent_service_account.member
}

resource "google_storage_bucket_iam_member" "spark_agent_service_account_object_admin_on_data_lake" {
  bucket = google_storage_bucket.data_lake.name
  role   = "roles/storage.objectAdmin"
  member = google_service_account.spark_agent_service_account.member
}

resource "google_artifact_registry_repository_iam_member" "spark_agent_service_account_python_artifact_reader" {
  project    = var.gcp_project_id
  location   = var.gcp_region
  repository = google_artifact_registry_repository.python.name
  role       = "roles/artifactregistry.reader"
  member     = google_service_account.spark_agent_service_account.member
}

resource "google_storage_bucket" "spark_staging" {
  name     = "spark-staging-${var.gcp_project_id}"
  location = var.gcp_region

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = false
  }

  force_destroy = true
}

resource "google_storage_bucket" "spark_temp" {
  name     = "spark-temp-${var.gcp_project_id}"
  location = var.gcp_region

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = false
  }

  force_destroy = true
}

resource "google_storage_bucket_object" "initialization-action-pip-packages" {
  name   = "initialization-actions/pip-packages.sh"
  source = "../spark/initialization-actions/pip-packages.sh"
  bucket = google_storage_bucket.spark_staging.name
}

resource "google_storage_bucket_object" "initialization-action-bigquery-connectors" {
  name   = "initialization-actions/bigquery-connectors.sh"
  source = "../spark/initialization-actions/bigquery-connectors.sh"
  bucket = google_storage_bucket.spark_staging.name
}

resource "google_dataproc_cluster" "spark_cluster" {
  name   = "spark-cluster"
  region = var.gcp_region

  cluster_config {
    staging_bucket = google_storage_bucket.spark_staging.name
    temp_bucket    = google_storage_bucket.spark_temp.name

    initialization_action {
      script      = "gs://${google_storage_bucket.spark_staging.name}/${google_storage_bucket_object.initialization-action-pip-packages.output_name}"
      timeout_sec = 600
    }

    initialization_action {
      script      = "gs://${google_storage_bucket.spark_staging.name}/${google_storage_bucket_object.initialization-action-bigquery-connectors.output_name}"
      timeout_sec = 600
    }

    gce_cluster_config {
      service_account = google_service_account.spark_agent_service_account.email
      service_account_scopes = [
        "cloud-platform"
      ]

      metadata = {
        "spark-bigquery-connector-url" : "gs://spark-lib/bigquery/spark-3.3-bigquery-0.29.0-preview.jar",
        "python-registry-project-id" : var.gcp_project_id,
        "python-registry-region" : var.gcp_region,
        "python-registry-name" : google_artifact_registry_repository.python.name
      }
    }

    master_config {
      num_instances = 1
      machine_type  = "e2-standard-2"

      disk_config {
        boot_disk_size_gb = 30
      }
    }

    worker_config {
      num_instances = 2
      machine_type  = "e2-standard-2"

      disk_config {
        boot_disk_size_gb = 30
      }
    }

    software_config {
      image_version = "2.1-debian11"

      override_properties = {
        "dataproc:dataproc.allow.zero.workers"    = "true",
        "dataproc:pip.packages"                   = "aqipy-atmotech==0.1.5",
        "spark:spark.jars.packages"               = "io.delta:delta-core_2.12:2.3.0",
        "spark:spark.sql.extensions"              = "io.delta.sql.DeltaSparkSessionExtension",
        "spark:spark.sql.catalog.spark_catalog"   = "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark:spark.bigquery.temporaryGcsBucket" = google_storage_bucket.spark_temp.name
      }
    }

    preemptible_worker_config {
      num_instances = 0
    }
  }

  depends_on = [
    google_project_service.required_services,
    google_project_iam_member.spark_agent_service_account_dataproc_worker,
    google_storage_bucket_object.initialization-action-pip-packages,
    google_storage_bucket_object.initialization-action-bigquery-connectors
  ]
}
