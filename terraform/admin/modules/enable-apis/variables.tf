variable "api_list" {
  description = "List of APIs to enable"
  type        = list(string)
}

variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
