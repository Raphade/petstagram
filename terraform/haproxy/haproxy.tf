variable "region" {
  type    = list(string)
  default = ["europe-west3"]
}
variable "zone" {
  type    = list(string)
  default = ["europe-west3-b"]
}

/*  Database server and Database  */
resource "google_sql_database_instance" "petstagram_db" {
  name             = "petstagram"
  database_version = "POSTGRES_15"
  region           = var.region
  root_password    = "s3cr3t!123"

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier      = "db-custom-2-4096"
    disk_size        = 10

    ip_configuration {
      ipv4_enabled        = true
       dynamic "authorized_networks" {
        for_each = google_compute_instance.petstagram_webserver
        iterator = petstagram_webserver

        content {
          name  = petstagram_webserver.value.name
          value = petstagram_webserver.value.network_interface.0.access_config.0.nat_ip
        }
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

/*  Network and Subnet  */
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

/*  The Webserver Instances  */

resource "google_compute_instance" "petstagram_webserver" {
  count        = 3
  name         = "petstagram_webserver-${count.index}"
  machine_type = "e2-small"
  zone         = var.zone
  network_interface {
    network = "default"
  }
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  metadata_startup_script = templatefile("./petstagram/startup.sh", {
    database_ip = google_compute_instance.petstagram_webserver[0].network_interface[0].network_ip
  })
}

resource "google_compute_instance" "haproxy" {
  name         = "haproxy-instance"
  machine_type = "e2-small"
  zone         = var.zone

  network_interface {
    network = "default"
  }
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }
  metadata_startup_script = templatefile("${path.module}/haproxy.sh", {
    webserver1_internal_ip = google_compute_instance.petstagram_webserver[0].network_interface[0].network_ip
    webserver2_internal_ip = google_compute_instance.petstagram_webserver[1].network_interface[0].network_ip
    webserver3_internal_ip = google_compute_instance.petstagram_webserver[2].network_interface[0].network_ip
  })
}

resource "google_compute_address" "public_ip" {
  name   = "webserver-ip"
  region = var.region
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
