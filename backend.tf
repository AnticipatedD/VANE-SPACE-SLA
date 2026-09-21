terraform {
  backend "s3" {
    bucket         = "vane-space-terraform-state-secure"
    key            = "prod/state.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "vane-space-lock-table"
  }
}
