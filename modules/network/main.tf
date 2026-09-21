resource "null_resource" "vpc_dummy" {
  triggers = {
    cidr = var.vpc_cidr
  }
}
