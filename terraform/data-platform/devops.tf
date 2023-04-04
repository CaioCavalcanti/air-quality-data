# See https://binx.io/2022/09/26/setup-keyless-authentication-to-google-cloud-for-github-actions-using-terraform/

resource "google_service_account" "devops_service_account" {
  account_id   = "sa-devops-agent"
  display_name = "DevOps Service Account"
}

resource "google_project_service" "iam_credentials" {
  project = var.gcp_project_id
  service = "iamcredentials.googleapis.com"
}

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
