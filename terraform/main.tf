terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2.1"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.2.0"
    }
  }
}

provider "null" {}

provider "docker" {}

module "root_telemetry" {
  source      = "./modules/telemetry"
  environment = "production"
}

resource "docker_image" "nginx" {
  name         = "docker.mirror.hashicorp.services/nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "tutorial"
  ports {
    internal = 80
    external = 8000
  }
}

output "telemetry_validation_status" {
  value       = module.telemetry.validation_id
  description = "Active deployment validation identifier from telemetry module"
}

output "nginx_container_name" {
  value       = docker_container.nginx.name
  description = "Name of the provisioned NGINX tutorial container"
}
