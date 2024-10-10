locals {
  lambda_iam_policy_name = "lambda_iam_policy"
  lambda_iam_policy_path = "./modules/iam/lambda-iam-policy.json"
  lambda_iam_role_name   = "lambda_iam_role"
  lambda_iam_role_path   = "./modules/iam/lambda-assume-role-policy.json"

  domain_name          = "stockreminderdomain.com"
  zone_id              = "Z02760782DJJH18ZS0A9U"
  domain_identity_type = "TXT"
  ttl                  = 600
  dkim_record_type     = "CNAME"

  # path_to_layer_source      = "../requirements/"
  # path_to_layer_artifact    = "../artifacts/requirements.zip"
  # requirements_layer_name   = "requirements"
  # compatible_layer_runtimes = ["python3.9"]
  # compatible_architectures  = ["x86_64"]

  archive_file_type        = "zip"
  path_to_source_directory = "../python/"
  path_to_artifact         = "../artifacts/lambda_function.zip"
  excluded_file            = "../python/main.py"
  function_name            = "lambda_function"
  function_handler         = "lambda_function.lambda_handler"
  memory_size              = 512
  timeout                  = 300
  runtime                  = "python3.9"
  event_rule_name          = "lambda-scheduler"
  schedule_expression      = "rate(1 day)"
  statement_id             = "AllowExecutionFromCloudWatch"
  cloudwatch_action        = "lambda:InvokeFunction"
  event_principal          = "events.amazonaws.com"

  aws_secrets_layer_name = "arn:aws:lambda:eu-west-2:133256977650:layer:AWS-Parameters-and-Secrets-Lambda-Extension:12"
}