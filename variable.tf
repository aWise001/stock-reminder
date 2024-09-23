variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

variable "s3_bucket_name" {
  type    = string
  default = "tfbackend-bucket"
}

variable "lambda_role_name" {
  type    = string
  default = "lambda_tf_role"
}

variable "lambda_policy_name" {
  type    = string
  default = "lambda_tf_policy"
}