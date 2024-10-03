variable "archive_file_type" {
  description = "type of archive to produce"
  type        = string
}

variable "lambda_iam_role_arn" {
  description = "Lambda IAM Role ARN"
  type        = string
}

variable "path_to_source_directory" {
  description = "Path to Lambda Fucntion Source Code"
  type        = string
}

variable "path_to_artifact" {
  description = "Path to ZIP artifact"
  type        = string
}

variable "excluded_file" {
  description = "file to be excluded from zip"
  type        = string
}

variable "function_name" {
  description = "Name of Lambda Function"
  type        = string
}

variable "function_handler" {
  description = "Name of Lambda Function Handler"
  type        = string
}

variable "memory_size" {
  description = "Lambda Memory"
  type        = number
}

variable "timeout" {
  description = "Lambda Timeout"
  type        = number
}

variable "runtime" {
  description = "Lambda Runtime"
  type        = string
}

variable "lambda_layer_arn" {
  description = "arn for lambda layer"
  type        = string
}

variable "aws_secrets_layer_name" {
  description = "name for the aws layer parameters and secrets extension"
  type        = string
}

variable "event_rule_name" {
  description = "name of cloudwatch event rule"
  type        = string
}

variable "schedule_expression" {
  description = "how often to schedule lambda"
  type        = string
}

variable "statement_id" {
  description = "unique statement identifier"
  type        = string
}

variable "cloudwatch_action" {
  description = "aws lambda action"
  type        = string
}

variable "event_principal" {
  description = "principal which is given permission"
  type        = string
}