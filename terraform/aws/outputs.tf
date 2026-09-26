output "document_bucket" {value = aws_s3_bucket.documents.id}
output "runtime_policy_arn" {value = aws_iam_policy.runtime.arn}
output "audit_log_group" {value = aws_cloudwatch_log_group.audit.name}
