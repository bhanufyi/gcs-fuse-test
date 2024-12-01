terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.12.0"
    }
  }

  backend "gcs" {
    bucket  = "bhanufyi-terraform-backend" # Replace with your bucket name
    prefix  = "terraform/admin"        # Folder structure in the bucket
  }
}

provider "google" {
  project = "bhanufyi"
  region  = "us-east1"
}
