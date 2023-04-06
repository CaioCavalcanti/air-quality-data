resource "google_artifact_registry_repository" "python" {
  location      = var.gcp_region
  repository_id = "python-${var.gcp_project_id}"
  format        = "PYTHON"

  depends_on = [
    google_project_service.required_services
  ]
}

resource "google_artifact_registry_repository" "docker" {
  location      = var.gcp_region
  repository_id = "docker-${var.gcp_project_id}"
  format        = "DOCKER"
}
