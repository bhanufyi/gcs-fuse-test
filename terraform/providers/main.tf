terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  backend "gcs" {
    bucket  = "bhanufyi-terraform-backend" # Replace with your bucket name
    prefix  = "terraform/state"        # Folder structure in the bucket
    location = "US-EAST1"              # Match the bucket's location
  }
}

provider "google" {
  project = "bhanufyi"
  region  = "us-east1"
}
