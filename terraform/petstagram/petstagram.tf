/*resource "google_compute_instance" "petstagram_webserver" {
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
*/

resource "google_sql_database_instance" "petstagram_db" {
  name             = "petstagram"
  database_version = "POSTGRES_15"
  region           = "europe-west3"
  root_password    = "s3cr3t!123"

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier                       = "db-custom-2-4096"
    disk_size = 10
    ip_configuration {
      ipv4_enabled        = true
      authorized_networks {
        name = "Public IP"
        value = google_compute_address.public_ip.address
        }
    }
  }
}

resource "google_sql_database" "database" {
  name     = "petstagram"
  instance = google_sql_database_instance.petstagram_db.name
}

resource "google_sql_user" "database_user" {
  name     = "django"
  instance = google_sql_database_instance.petstagram_db.name
  password = "s3cr3t!123"
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
  disk {
    boot              = true
    source_image      = "ubuntu-os-cloud/ubuntu-2204-lts"
    auto_delete       = true
  }
  metadata_startup_script = "${file("petstagram/startup.sh")}"
}

resource "google_compute_instance_group_manager" "webserver_group" {
  name        = "webserver_group"
  base_instance_name = "petstagram_webserver"
  target_size = 2
  zone        = "europe-west3-b"
    version {
    instance_template  = google_compute_instance_template.instance_template.self_link_unique
  }

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
    group = google_compute_instance_group_manager.webserver_group.self_link
  }
}


resource "google_compute_http_health_check" "health_check" {
  name                = "health-check"
  request_path       = "/"
  check_interval_sec  = 10
  timeout_sec         = 5
  healthy_threshold   = 2
  unhealthy_threshold = 2
  port                = 8080
}

resource "google_compute_target_pool" "target_pool" {
  name = "target-pool"
  region = "europe-west3"
  instances = [google_compute_instance_group_manager.webserver_group.instance_group]
  health_checks = [google_compute_http_health_check.health_check.self_link]
}

resource "google_compute_forwarding_rule" "forwarding_rule" {
  name        = "forwarding-rule"
  region      = "europe-west3"
  port_range  = "80"
  target      = google_compute_target_pool.target_pool.self_link
}
