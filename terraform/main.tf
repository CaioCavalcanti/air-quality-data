terraform {
  required_version = ">= 1.0"

  backend "gcs" {
  }

  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}
