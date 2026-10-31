# Connection Pool API

## Connection Pool Configuration

The connection pool controls how many network connections a client may create and reuse. The `maxPoolSize` setting limits the total number of active connections. The default value is 10.

## Connection Reset Errors

An `ECONNRESET` error means that the peer unexpectedly closed the network connection. Applications should retry idempotent operations with bounded backoff and avoid retry storms.

# Rolling Deployment API

## Rolling Update Configuration

The `maxUnavailable` setting controls how many replicas may be unavailable during a rolling update. Setting it to zero helps maintain capacity during heavy traffic, but may require additional temporary capacity.

## Zero-Downtime Upgrades

To reduce service interruption during upgrades, use readiness checks, gradual replacement, and a termination grace period. A deployment should remove an old instance only after a replacement is ready to receive traffic.

# Client Resource Protection

## Preventing Socket Starvation

Socket starvation occurs when all client connections remain occupied for too long. Use request timeouts, connection limits, and correct response-body cleanup so pooled connections can return to the available set.

