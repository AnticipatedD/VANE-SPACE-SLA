resource "null_resource" "telemetry_validation" {
  triggers = {
    service = "vane-space-sla"
  }
}
