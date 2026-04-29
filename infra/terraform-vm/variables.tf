variable "resource_group_name" {
  type    = string
  default = "rg-tp-vm"
}

variable "location" {
  type    = string
  default = "swedencentral"
}

variable "vm_name" {
  type    = string
  default = "Test-API"
}

variable "vm_size" {
  type    = string
  default = "Standard_B2ls_v2"
}

variable "admin_username" {
  type    = string
  default = "azureuser"
}

variable "ssh_public_key_path" {
  type    = string
  default = "~/.ssh/id_rsa.pub"
}
