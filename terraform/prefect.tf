resource "google_storage_bucket" "prefect_flows" {
  name     = "prefect-flows-${var.gcp_project_id}"
  location = var.gcp_region

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = false
  }

  force_destroy = true
}

resource "google_service_account" "prefect_agent_service_account" {
  account_id   = "sa-prefect-agent"
  display_name = "Prefect Agent Service Account"
}

resource "google_artifact_registry_repository_iam_member" "prefect_agent_service_account_reader_on_docker_repository" {
  project    = google_artifact_registry_repository.docker.project
  location   = google_artifact_registry_repository.docker.location
  repository = google_artifact_registry_repository.docker.name
  role       = "roles/artifactregistry.reader"
  member     = google_service_account.prefect_agent_service_account.member
}

resource "google_storage_bucket_iam_member" "prefect_agent_service_account_reader_on_prefect_flows" {
  bucket = google_storage_bucket.prefect_flows.name
  role   = "roles/storage.objectViewer"
  member = google_service_account.prefect_agent_service_account.member
}

resource "google_project_iam_member" "prefect_agent_service_account_dataproc_worker" {
  project = var.gcp_project_id
  role    = "roles/dataproc.editor"
  member  = google_service_account.prefect_agent_service_account.member
}

resource "google_storage_bucket_iam_member" "prefect_agent_service_account_reader_on_spark_staging" {
  bucket = google_storage_bucket.spark_staging.name
  role   = "roles/storage.objectViewer"
  member = google_service_account.prefect_agent_service_account.member
}

resource "google_storage_bucket_iam_member" "prefect_agent_service_account_object_admin_on_data_lake" {
  bucket = google_storage_bucket.data_lake.name
  role   = "roles/storage.objectAdmin"
  member = google_service_account.prefect_agent_service_account.member
}

# GCS block on Prefect requires the permission storage.buckets.get
# Consider creating a custom role if needed.
resource "google_storage_bucket_iam_member" "prefect_agent_service_account_legacy_bucket_reader_on_data_lake" {
  bucket = google_storage_bucket.data_lake.name
  role   = "roles/storage.legacyBucketReader"
  member = google_service_account.prefect_agent_service_account.member
}
