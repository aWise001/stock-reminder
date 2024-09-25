data "archive_file" "zip_file" {
  type        = "zip"
  output_path = var.path_to_artifact

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