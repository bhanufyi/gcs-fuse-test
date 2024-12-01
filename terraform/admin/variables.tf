variable "api_list" {
  default = [
    "compute.googleapis.com",
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "storage.googleapis.com",
	"serviceusage.googleapis.com"
  ]
}

variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
  default = "bhanufyi"
}

variable "service_account_id" {
  default = "ai-ml-sa"
}

variable "service_account_display_name" {
  default = "AI/ML Test Service Account"
}

variable "service_account_roles" {
  default = [
    "roles/storage.objectAdmin",
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/artifactregistry.admin"
  ]
}