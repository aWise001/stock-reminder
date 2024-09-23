resource "aws_s3_bucket" "s3_bucket_backend" {
  bucket = var.s3_bucket_name
}

resource "aws_s3_bucket_acl" "s3_bucket_backend_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership]
  bucket     = aws_s3_bucket.s3_bucket_backend.id
  acl        = "private"
}

resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
  bucket = aws_s3_bucket.s3_bucket_backend.id
  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_versioning" "s3_bucket_version" {
  bucket = aws_s3_bucket.s3_bucket_backend.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_object" "terraform_folder" {
  bucket = aws_s3_bucket.s3_bucket_backend.id
  key    = "terraform.tfstate"
}

resource "aws_s3_bucket_public_access_block" "s3_bucket_access" {
  bucket                  = aws_s3_bucket.s3_bucket_backend.bucket
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "archive_file" "lambda_archive_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/"
  output_path = "${path.module}/lambda/main.zip"
}

resource "aws_lambda_function" "lambda" {
  description      = "Lambda Function"
  filename         = join("", data.archive_file.lambda_archive_file.*.output_path)
  function_name    = "tf-stock-reminder"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.lambda_handler"
  source_code_hash = join("", data.archive_file.lambda_archive_file.*.output_base64sha256)
  runtime          = "python3.9"
}

resource "aws_cloudwatch_log_group" "lambda_loggroup" {
  name              = "/aws/lambda/logs"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "codebuild_loggroup" {
  name              = "/aws/codebuild/logs"
  retention_in_days = 14
}