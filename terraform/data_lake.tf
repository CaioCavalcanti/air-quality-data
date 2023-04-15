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

resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.data_lake.name
  role   = "roles/storage.objectAdmin"
  member = google_service_account.prefect_agent_service_account.member
}

resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.data_lake.name
  role   = "roles/storage.objectAdmin"
  member = google_service_account.spark_agent_service_account.member
}
