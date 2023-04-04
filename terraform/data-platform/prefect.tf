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

data "google_iam_policy" "prefect_flows_policy" {
  binding {
    role = "roles/storage.objectViewer"

    members = [
      google_service_account.prefect_agent_service_account.member
    ]
  }
}

resource "google_storage_bucket_iam_policy" "prefect_flows" {
  bucket      = google_storage_bucket.prefect_flows.name
  policy_data = data.google_iam_policy.prefect_flows_policy.policy_data
}
