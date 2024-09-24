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

module "lambdaFunction" {
  source = "./modules/lambda"

  lambda_iam_role_arn = module.lambdaIAM.lambda_iam_role_arn
  path_to_source_file = local.path_to_source_file
  path_to_artifact    = local.path_to_artifact
  function_name       = local.function_name
  function_handler    = local.function_handler
  memory_size         = local.memory_size
  timeout             = local.timeout
  runtime             = local.runtime
}