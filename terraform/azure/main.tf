resource "random_string" "suffix" {length = 6; special = false; upper = false}
locals {name = "enterprise-rag-${var.environment}-${random_string.suffix.result}"}
resource "azurerm_resource_group" "main" {name = "rg-${local.name}"; location = var.location}
resource "azurerm_cognitive_account" "openai" {
  name = "aoai-${local.name}"
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind = "OpenAI"
  sku_name = "S0"
  custom_subdomain_name = "aoai-${local.name}"
  local_auth_enabled = false
  public_network_access_enabled = false
}
resource "azurerm_search_service" "rag" {
  name = "search-${local.name}"
  resource_group_name = azurerm_resource_group.main.name
  location = azurerm_resource_group.main.location
  sku = "basic"
  local_authentication_enabled = false
  public_network_access_enabled = false
}
resource "azurerm_key_vault" "rag" {
  name = "kv-rag-${random_string.suffix.result}"
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id = data.azurerm_client_config.current.tenant_id
  sku_name = "standard"
  enable_rbac_authorization = true
  purge_protection_enabled = true
}
data "azurerm_client_config" "current" {}
resource "azurerm_application_insights" "rag" {
  name = "appi-${local.name}"
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type = "web"
}
