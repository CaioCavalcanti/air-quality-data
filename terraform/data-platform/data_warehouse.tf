resource "google_bigquery_dataset" "raw_dataset" {
  dataset_id = "Raw"
  location   = var.gcp_region
}

resource "google_bigquery_dataset_iam_member" "editor" {
  dataset_id = google_bigquery_dataset.raw_dataset.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = google_service_account.spark_agent_service_account.member
}
