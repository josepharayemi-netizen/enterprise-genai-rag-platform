output "openai_endpoint" {value = azurerm_cognitive_account.openai.endpoint}
output "search_endpoint" {value = "https://${azurerm_search_service.rag.name}.search.windows.net"}
output "key_vault_uri" {value = azurerm_key_vault.rag.vault_uri}
