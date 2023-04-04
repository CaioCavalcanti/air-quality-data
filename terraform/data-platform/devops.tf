locals {
  required_services = [
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "artifactregistry.googleapis.com",
    "dataproc.googleapis.com"
  ]
}

resource "google_project_service" "required_services" {
  for_each = toset(local.required_services)
  project  = var.gcp_project_id
  service  = each.key
}

resource "google_service_account" "devops_service_account" {
  account_id   = "sa-devops-agent"
  display_name = "DevOps Service Account"
}

resource "google_project_iam_member" "devops_service_account_editor" {
  project = var.gcp_project_id
  role    = "roles/editor"
  member  = google_service_account.devops_service_account.member
}

# See https://binx.io/2022/09/26/setup-keyless-authentication-to-google-cloud-for-github-actions-using-terraform/
resource "google_iam_workload_identity_pool" "devops" {
  workload_identity_pool_id = "devops"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.devops.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"

  attribute_mapping = {
    "google.subject"       = "assertion.sub",
    "attribute.actor"      = "assertion.actor",
    "attribute.repository" = "assertion.repository"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_member" "github_workload_identity_user" {
  service_account_id = google_service_account.devops_service_account.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.devops.name}/attribute.repository/${var.github_repository}"
}

data "google_storage_bucket" "tfstate" {
  name = var.gcp_gcs_tfstate_bucket_name
}
