# CERT-MANAGER

The [Cert-Manager](https://github.com/jetstack/cert-manager) is a component that allows automatic management of TLS artifacts, it supports many issuers and has been progressively polished as one of the most featureful solutions in this space.

## Main course

It can be found in the `base` directory: it contains a minimal install of Cert Manager with mostly upstream settings.

## Toppings

Replace all references to `bob` with your own head-waiter's name.

### ca-issuer

The CA issuer deploys a CA certificate and a cluster issuer using it.

It can be used to establish mutual TLS authentication for in-cluster workloads (think databases) or to secure intranet portals.

### letsencrypt-issuer

This example deploys a Letsencrypt issuer leveraging HTTP01 verification, please be aware that if you have access to DNS modifications you should use the DNS challenge instead and grab wildcard certificates.
Cert-manager docs can point you in the right direction
