terraform {
  backend "s3" {
    bucket         = "stock-reminder-tf-state-backend"
    key            = "tf-infra/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "terraform-state-locking"
    encrypt        = true
  }

  required_version = ">=0.13.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>3.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

# module "tf-state" {
#   source      = "./modules/tf-state"
#   bucket_name = "stock-reminder-tf-state-backend"
# }

module "lambdaIAM" {
  source = "./modules/iam"

  lambda_iam_policy_name = local.lambda_iam_policy_name
  lambda_iam_policy_path = local.lambda_iam_policy_path
  lambda_iam_role_name   = local.lambda_iam_role_name
  lambda_iam_role_path   = local.lambda_iam_role_path
}

module "ses" {
  source = "./modules/ses"

  domain_name          = local.domain_name
  zone_id              = local.zone_id
  domain_identity_type = local.domain_identity_type
  ttl                  = local.ttl
  dkim_record_type     = local.dkim_record_type
}

# module "lambda_layer" {
#   source = "./modules/lambda_layer"

#   path_to_layer_source      = local.path_to_layer_source
#   path_to_layer_artifact    = local.path_to_layer_artifact
#   requirements_layer_name   = local.requirements_layer_name
#   compatible_layer_runtimes = local.compatible_layer_runtimes
#   compatible_architectures  = local.compatible_architectures
# }

module "lambdaFunction" {
  source = "./modules/lambda"

  archive_file_type        = local.archive_file_type
  lambda_iam_role_arn      = module.lambdaIAM.lambda_iam_role_arn
  path_to_source_directory = local.path_to_source_directory
  path_to_artifact         = local.path_to_artifact
  excluded_file            = local.excluded_file
  function_name            = local.function_name
  function_handler         = local.function_handler
  memory_size              = local.memory_size
  timeout                  = local.timeout
  runtime                  = local.runtime
  lambda_layer_arn         = module.lambda_layer.requirements_layer_arn
  aws_secrets_layer_name   = local.aws_secrets_layer_name
  event_rule_name          = local.event_rule_name
  schedule_expression      = local.schedule_expression
  statement_id             = local.statement_id
  cloudwatch_action        = local.cloudwatch_action
  event_principal          = local.event_principal
}