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

resource "google_storage_bucket_iam_member" "prefect_agent_service_account_reader_on_prefect_flows" {
  bucket = google_storage_bucket.prefect_flows.name
  role   = "roles/storage.objectViewer"
  member = google_service_account.prefect_agent_service_account.member
}

resource "google_artifact_registry_repository_iam_member" "prefect_agent_service_account_reader_on_docker_repository" {
  project    = google_artifact_registry_repository.docker.project
  location   = google_artifact_registry_repository.docker.location
  repository = google_artifact_registry_repository.docker.name
  role       = "roles/artifactregistry.reader"
  member     = google_service_account.devops_service_account.member
}


# resource "google_sql_database_instance" "prefect" {
#   name                = "prefect"
#   database_version    = "POSTGRES_14"
#   region              = var.gcp_region
#   # deletion_protection = false

#   settings {
#     tier = "db-f1-micro"
#   }
# }
