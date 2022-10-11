variable "gcp_credentials" {
  description = "Sensitive ENV variables for GCP only"
  type        = string
  sensitive   = true
}

variable "gcp_sa_email" {
  description = "GCP Sentitive service account email"
  type        = string
  sensitive   = true
}

variable "gcp_project" {
  description = "GCP Sensitive project"
  type        = string
  sensitive   = true
}

variable "gcp_region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}
