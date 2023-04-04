resource "google_artifact_registry_repository" "python" {
  location      = var.gcp_region
  repository_id = "python-${var.gcp_project_id}"
  format        = "PYTHON"

  depends_on = [
    google_project_service.required_services
  ]
}

resource "google_artifact_registry_repository_iam_member" "devops_sa_python_writer" {
  project    = google_artifact_registry_repository.python.project
  location   = google_artifact_registry_repository.python.location
  repository = google_artifact_registry_repository.python.name
  role       = "roles/artifactregistry.writer"
  member     = google_service_account.devops_service_account.member
}
