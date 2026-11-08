# Deployment Runbook

## Pre-deployment checks

Confirm that the change has passed automated tests, required approvals, configuration validation, and security review. Verify that the target environment and release version are correct.

## Deployment sequence

Build an immutable artifact, deploy it to the selected environment, run health checks, and monitor error rate and latency during the rollout. Use a canary or gradual rollout for high-risk changes.

## Rollback

If health checks fail or key metrics regress, stop the rollout and restore the last known-good artifact. Record the incident, observed symptoms, and recovery actions.

