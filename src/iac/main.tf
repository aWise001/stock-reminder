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

module "tf-state" {
  source      = "./modules/tf-state"
  bucket_name = "stock-reminder-tf-state-backend"
}