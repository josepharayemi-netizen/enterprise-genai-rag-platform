# Production Deployment Policy

Production deployments require a successful quality evaluation, security scan, named service owner and human approval. GitOps applies the approved immutable image digest. Pull requests cannot deploy directly to production. Rollback uses the previously approved Git commit and image digest.

Every workload uses short-lived identity. Secrets must be stored in AWS Secrets Manager or Azure Key Vault and must never be committed to source control.
