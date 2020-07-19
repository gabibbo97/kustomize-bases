# Storage recipes

Storage contains all that is needed to persist your data in Kubernetes

## Ingredients

### Local path provisioner

Local path provisioner assolves the role of `simply mount a folder in a container`.

Very simple, light on resources but with the drawbacks of being bound to the node the workload was scheduled on and with no replication / scale out facilities.

Recommended for IoT or workloads that can manage their own replication (databases, ...)
