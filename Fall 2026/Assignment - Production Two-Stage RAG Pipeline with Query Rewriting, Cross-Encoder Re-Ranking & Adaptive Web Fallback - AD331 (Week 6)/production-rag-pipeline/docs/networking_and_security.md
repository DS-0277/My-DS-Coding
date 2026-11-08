# Networking and Security

## Network design

Use private subnets for internal services and restrict inbound traffic to approved sources. Public endpoints should terminate TLS and pass through authentication and rate limiting.

## Identity and access

Service identities should receive only the permissions required for their function. Secrets belong in a managed secret store or protected environment variables, never in source control.

## Defensive controls

Log authentication failures, protect administrative endpoints, validate external inputs, and review dependency updates for known vulnerabilities.

