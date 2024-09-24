locals {
  lambda_iam_policy_name = "lambda_iam_policy"
  lambda_iam_policy_path = "./modules/iam/lambda-iam-policy.json"
  lambda_iam_role_name   = "lambda_iam_role"
  lambda_iam_role_path   = "./modules/iam/lambda-assume-role-policy.json"

  path_to_source_file = "../python/lambda_function.py"
  path_to_artifact    = "../main.zip"
  function_name       = "lambda_function"
  function_handler    = "lambda_function.lambda_handler"
  memory_size         = 512
  timeout             = 300
  runtime             = "python3.9"
}