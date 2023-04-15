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
