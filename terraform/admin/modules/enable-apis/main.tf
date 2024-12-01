resource "google_project_service" "enable_services" {
  for_each = toset(var.api_list)

  project = var.project_id
  service = each.value
  lifecycle {
    prevent_destroy = true
  }

}
