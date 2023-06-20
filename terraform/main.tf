provider "google" {
    project = "petstagram-389018"
    credentials = "${file("credentials.json")}"
    region = "europe-west3"
    zone = "europe-west3-b"
}

variable "deployment_type" {
  type    = string
  default = "gcloud"
}

module "petstagram" {
  count = var.deployment_type == "gcloud" ? 1 : 0 # if deployment_type == gcloud, deploy 1 instance of this module, else 0
  source = "./petstagram"
  providers = {
    google = google
  }
}

module "haproxy" {
  count = var.deployment_type == "haproxy" ? 1 : 0 # if deployment_type == haproxy, deploy 1 instance of this module, else 0
  source = "./haproxy"
  providers = {
    google = google
  }
}