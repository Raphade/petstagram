provider "google" {
    project = "petstagram-389018"
    credentials = "${file("credentials.json")}"
    region = "europe-west3"
    zone = "europe-west3-b"
}

module "petstagram" {
  source = "./petstagram"
}

module "haproxy" {
  source = "./haproxy"
}