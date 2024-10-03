variable "path_to_layer_source" {
  description = "path to layer source files"
  type        = string
}

variable "path_to_layer_artifact" {
  description = "path to zip file destination"
  type        = string
}

variable "requirements_layer_name" {
  description = "name of layer"
  type        = string
}

variable "compatible_layer_runtimes" {
  description = "runtime version"
  type        = list(string)
}

variable "compatible_architectures" {
  description = "architecture type"
  type        = list(string)
}