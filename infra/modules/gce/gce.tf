resource "google_compute_instance" "thumborizeme" {
  name         = "thumborizeme-be"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  tags = ["http-server", "https-server"]

  boot_disk {
    initialize_params {
      image = "debian-11-bullseye-v20220920"
      size  = 10
    }
  }

  network_interface {
    network    = "thumborizeme-vpc"
    subnetwork = "thumborizeme-subnet"

    access_config {
      // Ephemeral public IP
    }
  }

  metadata = {
    foo = "bar"
  }

  metadata_startup_script = <<EOT
  #!/bin/bash
  apt update -y
  apt install -y ansible
  mkdir -p /opt/ansible
  curl https://https://raw.githubusercontent.com/thumbor/thumborizeme/thumborizeme-gcp/playbook.yml -o /opt/ansible/playbook.yml
  ansible-playbook /opt/ansible/playbook.yml -t utils,web,redis
  EOT

  #service_account {
  #  # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
  #  email  = var.sa_email
  #  scopes = ["cloud-platform"]
  #}
}
