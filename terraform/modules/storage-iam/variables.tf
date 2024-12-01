variable "bucket_name" {
  description = "Name of the bucket"
  type        = string
}

variable "role" {
  description = "IAM role to assign"
  type        = string
}

variable "members" {
  description = "List of members to bind to the role"
  type        = list(string)
}
