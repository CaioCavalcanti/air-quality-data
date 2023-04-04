resource "google_storage_bucket" "data_lake" {
  name     = "data-lake-${var.gcp_project_id}"
  location = var.gcp_region

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }

  force_destroy = true
}

data "google_iam_policy" "data_lake_policy" {
  binding {
    role = "roles/storage.objectViewer"

    members = [
      google_service_account.prefect_agent_service_account.member,
      google_service_account.spark_agent_service_account.member
    ]
  }

  binding {
    role = "roles/storage.legacyBucketReader"

    members = [
      google_service_account.prefect_agent_service_account.member
    ]
  }
}

resource "google_storage_bucket_iam_policy" "data_lake" {
  bucket      = google_storage_bucket.data_lake.name
  policy_data = data.google_iam_policy.data_lake_policy.policy_data
}
