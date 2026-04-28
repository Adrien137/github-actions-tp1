variable "project_name" {
  type    = string
  default = "fil-rouge-task-api"
}

variable "location" {
  type    = string
  default = "France Central"
}

variable "resource_group_name" {
  type    = string
  default = "rg-fil-rouge-task-api"
}

variable "acr_name" {
  type        = string
  description = "Nom unique globalement pour Azure Container Registry. Exemple : acrtaskapi12345"
}

variable "webapp_name" {
  type        = string
  description = "Nom unique globalement pour Azure Web App. Exemple : webapp-task-api-12345"
}
