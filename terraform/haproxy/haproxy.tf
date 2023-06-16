provider "google" {
    project = "petstagram-389018"
    credentials = "${file("./credentials.json")}"
    region = "europe-west3"
    zone = "europe-west3-b"
}

resource "google_compute_instance" "webserver" {
  count        = 3
  name         = "webserver-${count.index}"
  machine_type = "e2-small"
  zone         = "europe-west3-b"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  metadata_startup_script = file("startup.sh")
}

resource "google_compute_instance" "haproxy" {
  name         = "haproxy-instance"
  machine_type = "e2-small"
  zone         = "europe-west3-b"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }
  metadata_startup_script = templatefile("${path.module}/haproxy.sh", {
    webserver1_internal_ip = google_compute_instance.webserver[0].network_interface[0].network_ip
    webserver2_internal_ip = google_compute_instance.webserver[1].network_interface[0].network_ip
    webserver3_internal_ip = google_compute_instance.webserver[2].network_interface[0].network_ip
  })
}

resource "google_compute_address" "public_ip" {
  name   = "webserver-ip"
  region = "europe-west3"
}

resource "google_compute_firewall" "allow_http" {
  name    = "allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
}

resource "google_compute_firewall" "allow_haproxy" {
  name    = "allow-haproxy"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }
}

output "webserver_ip" {
  value = google_compute_address.public_ip.address
}