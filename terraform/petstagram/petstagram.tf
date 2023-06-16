provider "google" {
    project = "petstagram-389018"
    credentials = "${file("./credentials.json")}"
    region = "europe-west3"
    zone = "europe-west3-b"
}

resource "google_compute_instance" "vm_instance" {
  count        = 3
  name         = "petstagram_webserver-${count.index}"
  machine_type = "e2-small"
  zone         = "europe-west3-b"
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }
  metadata_startup_script = "${file("startup.sh")}"
}

resource "google_compute_address" "public_ip" {
  name = "webserver-ip"
  region = "europe-west3"
}

resource "google_compute_backend_service" "backend_service" {
  name             = "backend-service"
  protocol         = "HTTP"
  port_name        = "http"
  timeout_sec      = 30

  backend {
    group = google_compute_instance_group.vm_group.self_link
  }
}

resource "google_compute_health_check" "health_check" {
  name                = "health-check"
  request_path       = "/"
  check_interval_sec  = 10
  timeout_sec         = 5
  healthy_threshold   = 2
  unhealthy_threshold = 2

  http_health_check {
    port = 8000
  }
}

resource "google_compute_instance_template" "instance_template" {
  name                    = "instance-template"
  machine_type            = "e2-small"
  can_ip_forward          = true
  region                  = "europe-west3"
  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.public_ip.address
    }
  }
  disks {
    boot = true
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }
  metadata_startup_script = google_compute_instance.webserver.metadata_startup_script
}

resource "google_compute_instance_group" "webserver_group" {
  name        = "webserver-group"
  zone        = "europe-west3-b"
  description = "Webserver Instance Group"
  instances   = google_compute_instance.webserver.*.self_link
}

resource "google_compute_target_pool" "target_pool" {
  name = "target-pool"
  region = "europe-west3"
  instances = google_compute_instance_group.webserver_group.instances
  health_checks = [google_compute_health_check.health_check.self_link]
}

resource "google_compute_forwarding_rule" "forwarding_rule" {
  name        = "forwarding-rule"
  region      = "europe-west3"
  port_range  = "80"
  target      = google_compute_target_pool.target_pool.self_link
}

resource "google_sql_database_instance" "database_instance" {
  name             = "petstagram-db"
  database_version = "POSTGRES_12"
  region           = "europe-west3"
  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "database" {
  name     = "petstagram"
  instance = google_sql_database_instance.database_instance.name
}

resource "google_compute_forwarding_rule" "forwarding_rule" {
  name        = "forwarding-rule"
  region      = "europe-west3"
  port_range  = "80"
  target      = google_compute_target_pool.target_pool.self_link
}