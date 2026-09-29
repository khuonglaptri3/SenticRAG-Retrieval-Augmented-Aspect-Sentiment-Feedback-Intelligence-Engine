# Artifact Storage Conventions

This directory represents the local convention for training artifacts.

In production:
- Large binary artifacts (model weights, PhoBERT checkpoints, vector indices) are **versioned and stored in AWS S3**:
  `s3://ai-artifacts/project-a/sentiment/<run_id>/`
- Each run produces an immutable `run-manifest.json` capturing git SHA, dataset version, container digest, and evaluation metrics.
- Binary files must **never be committed to Git**.
