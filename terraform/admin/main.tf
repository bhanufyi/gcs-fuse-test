module "enable_apis" {
  source    = "./modules/enable-apis"
  api_list  = var.api_list
  project_id = var.project_id
}

module "service_account" {
  source      = "./modules/service-account"
  account_id  = var.service_account_id
  display_name = var.service_account_display_name
  project_id  = var.project_id
  roles       = var.service_account_roles
}
