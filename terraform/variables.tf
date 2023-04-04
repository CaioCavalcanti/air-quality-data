variable "gcp_project_id" {
  description = "The Google Cloud Platform (GCP) Project ID."
  type        = string
}

variable "gcp_region" {
  description = "The GCP region where the resources will be created."
  type        = string
}

variable "github_repository" {
  description = "The GitHub repository name to authorize for GitHub Actions."
  type        = string
  default     = "CaioCavalcanti/air-quality-data"
}
