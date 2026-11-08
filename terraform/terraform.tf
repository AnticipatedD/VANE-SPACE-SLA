terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.2.0"
    }
  }
  required_version = "~> 1.7"
}

provider "docker" {
  host = var.docker_host
}

variable "docker_host" {
  type        = string
  description = "Docker daemon socket address"
  default     = "unix:///var/run/docker.sock"
}

resource "docker_image" "vane_space_engine" {
  name         = "vane-space-engine:latest"
  keep_locally = true
}

resource "docker_container" "vane_space_service" {
  image = docker_image.vane_space_engine.image_id
  name  = "vane-space-service"
  ports {
    internal = 8080
    external = 8080
  }
  env = [
    "ENVIRONMENT=production"
  ]
}

output "container_id" {
  value       = docker_container.vane_space_service.id
  description = "The ID of the deployed Vane Space container"
}
