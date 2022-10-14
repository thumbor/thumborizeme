terraform {
}

module "thumborize-gce" {
  source = "../modules/gce"

  sa_email    = var.gcp_sa_email
  project     = var.gcp_project
  region      = var.gcp_region
  credentials = var.gcp_credentials
}

