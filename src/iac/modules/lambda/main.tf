data "archive_file" "zip_file" {
  type        = var.archive_file_type
  output_path = var.path_to_artifact
  excludes = [ var.excluded_file ]

  source_dir = var.path_to_source_directory
}

resource "aws_lambda_function" "stock_reminder_lambda" {
  filename      = var.path_to_artifact
  function_name = var.function_name
  role          = var.lambda_iam_role_arn
  handler       = var.function_handler

  memory_size = var.memory_size
  timeout     = var.timeout

  depends_on = [ data.archive_file.zip_file ]

  source_code_hash = filebase64sha256(var.path_to_artifact)

  runtime = var.runtime

  layers = [var.aws_secrets_layer_name]
}

resource "aws_cloudwatch_event_rule" "lambda_scheduler" {
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "event_target" {
  rule = aws_cloudwatch_event_rule.lambda_scheduler.name
  arn  = aws_lambda_function.stock_reminder_lambda.arn
}

resource "aws_lambda_permission" "cloudwatch_permission" {
  statement_id = var.statement_id
  action = var.cloudwatch_action
  function_name = aws_lambda_function.stock_reminder_lambda.function_name
  principal = var.event_principal
  source_arn = aws_cloudwatch_event_rule.lambda_scheduler.arn
}