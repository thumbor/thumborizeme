variable "project" {
  description = "Project name"
  type        = string
}

variable "region" {
  description = "Region name"
  type        = string
}

variable "sa_email" {
  description = "Service account email"
  sensitive   = true
  type        = string
}

variable "credentials" {
  type        = string
  sensitive   = true
  description = "Sensitive Google Cloud service account credentials"
}
