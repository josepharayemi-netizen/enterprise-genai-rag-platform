locals {name = "enterprise-rag-${var.environment}"}
resource "aws_kms_key" "rag" {description = "RAG data encryption"; enable_key_rotation = true}
resource "aws_s3_bucket" "documents" {bucket_prefix = "${local.name}-documents-"}
resource "aws_s3_bucket_public_access_block" "documents" {
  bucket = aws_s3_bucket.documents.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_server_side_encryption_configuration" "documents" {
  bucket = aws_s3_bucket.documents.id
  rule {apply_server_side_encryption_by_default {sse_algorithm = "aws:kms"; kms_master_key_id = aws_kms_key.rag.arn}}
}
resource "aws_cloudwatch_log_group" "audit" {
  name = "/${local.name}/audit"
  retention_in_days = 30
  kms_key_id = aws_kms_key.rag.arn
}
data "aws_iam_policy_document" "runtime" {
  statement {
    actions = ["bedrock:InvokeModel"]
    resources = [var.bedrock_model_arn]
  }
  statement {
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.documents.arn}/*"]
  }
}
resource "aws_iam_policy" "runtime" {name = "${local.name}-runtime"; policy = data.aws_iam_policy_document.runtime.json}
