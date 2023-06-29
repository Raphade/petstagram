variable "region" {
  type    = string
  default = "europe-west3"
}
variable "zone" {
  type    = string
  default = "europe-west3-b"
}

/*resource "google_compute_instance" "petstagram_webserver" {
  count        = 3
  name         = "petstagram_webserver-${count.index}"
  machine_type = "e2-small"
  zone         = var.zone
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }
  metadata_startup_script = "${file("startup.sh")}"
}
*/


/*  Network Infrastructure  */
resource "google_compute_network" "default" {
  name                    = "default-network"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "default" {
  name                       = "backend-subnet"
  ip_cidr_range              = "10.1.2.0/24"
  network                    = google_compute_network.default.id
  private_ipv6_google_access = "DISABLE_GOOGLE_ACCESS"
  purpose                    = "PRIVATE"
  region                     = var.region
  stack_type                 = "IPV4_ONLY"
}

resource "google_compute_subnetwork" "proxy_only" {
  name          = "proxy-only-subnet"
  ip_cidr_range = "10.129.0.0/23"
  network       = google_compute_network.default.id
  purpose       = "REGIONAL_MANAGED_PROXY"
  region        = var.region
  role          = "ACTIVE"
}


/*  Firewalls  */
resource "google_compute_firewall" "default" {
  name = "fw-allow-health-check"
  allow {
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.default.id
  priority      = 1000
  source_ranges = ["130.211.0.0/22", "35.191.0.0/16"]
  target_tags   = ["load-balanced-backend"]
}

resource "google_compute_firewall" "allow_proxy" {
  name = "fw-allow-proxies"
  allow {
    ports    = ["443"]
    protocol = "tcp"
  }
  allow {
    ports    = ["80"]
    protocol = "tcp"
  }
  allow {
    ports    = ["8080"]
    protocol = "tcp"
  }
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.default.id
  priority      = 1000
  source_ranges = ["10.129.0.0/23", "35.235.240.0/20"]
  target_tags   = ["load-balanced-backend"]
}


/*  Database Instance and Database  */
resource "google_sql_database_instance" "petstagram_db" {
  name             = "petstagram"
  database_version = "POSTGRES_15"
  region           = var.region
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
  deletion_protection = false
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

data "google_compute_image" "ubuntu_image" {
  family  = "ubuntu-2204-lts"
  project = "ubuntu-os-cloud"
}

/*  Instance Template and managed Instance Group  */
resource "google_compute_instance_template" "instance_template" {
  name                    = "instance-template"
  machine_type            = "e2-small"
  can_ip_forward          = true
  region                  = var.region
  tags                    = ["load-balanced-backend"]
  network_interface {
    network    = google_compute_network.default.id
    subnetwork = google_compute_subnetwork.default.id
  }
  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    provisioning_model  = "STANDARD"
  }
  disk {
    boot              = true
    source_image      = data.google_compute_image.ubuntu_image.self_link
    auto_delete       = true
    type              = "PERSISTENT"
  }
  metadata_startup_script = "${file("petstagram/startup.sh")}"
}

resource "google_compute_instance_group_manager" "webserver-group" {
  name               = "webserver-group"
  base_instance_name = "petstagram-webserver"
  target_size        = 2
  zone                = var.zone
  named_port {
    name = "http"
    port = 80
  }
    version {
    instance_template  = google_compute_instance_template.instance_template.id
    name               = "primary"
  }

}


/*  IP adress for the Load Balancer  */
resource "google_compute_address" "public_ip" {
  name = "webserver-ip"
  address_type = "EXTERNAL"
  network_tier = "STANDARD"
  region = var.region
}

/*  Backend and with managed Instacegroup   */

resource "google_compute_region_backend_service" "backend" {
  name                  = "backend-service"
  region                = var.region
  load_balancing_scheme = "EXTERNAL_MANAGED"
  health_checks         = [google_compute_region_health_check.health_check.id]
  protocol              = "HTTP"
  session_affinity      = "NONE"
  timeout_sec           = 30
  backend {
    group           = google_compute_instance_group_manager.webserver-group.instance_group
    balancing_mode  = "UTILIZATION"
    capacity_scaler = 1.0
  }
}

resource "google_compute_region_health_check" "health_check" {
  name                = "health-check"
  check_interval_sec  = 10
  timeout_sec         = 5
  healthy_threshold   = 2
  unhealthy_threshold = 2
  http_health_check {
    port_specification = "USE_SERVING_PORT"
    proxy_header       = "NONE"
    request_path       = "/"

  }
  
}

resource "google_compute_region_url_map" "map" {
  name            = "map"
  region          = var.region
  default_service = google_compute_region_backend_service.backend.id
}

resource "google_compute_region_target_http_proxy" "proxy" {
  name    = "proxy"
  region  = var.region
  url_map = google_compute_region_url_map.map.id
}

resource "google_compute_forwarding_rule" "forwarding_rule" {
  name                  = "forwarding-rule"
  depends_on            = [google_compute_subnetwork.proxy_only]
  region                = var.region
  port_range            = "80"
  ip_protocol           = "TCP"
  ip_address            = google_compute_address.public_ip.id
  network               = google_compute_network.default.id
  target                = google_compute_region_target_http_proxy.proxy.id
  load_balancing_scheme = "EXTERNAL_MANAGED"
  network_tier          = "STANDARD"
}

output "public_ip" {
  value = google_compute_address.public_ip.address
}
