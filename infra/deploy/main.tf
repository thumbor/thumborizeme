terraform {
  # terraform init --backend-config="username=tsuru_token" --backend-config="password=$(cat ~/.tsuru/token)" -reconfigure
}

locals {
  env       = "qa01"
  log_level = "info"
}

module "thumborize-gce" {
  source = "../modules/gce"

  sa_email         = var.gcp_sa_email
  project       = var.gcp_project
  region        = var.gcp_region
  credentials   = var.gcp_credentials
}

