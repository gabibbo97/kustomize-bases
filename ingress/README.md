# Ingress recipes

[https://kubernetes.io/docs/concepts/services-networking/ingress](Ingress) is the resource delegated to configure L7 HTTP access to your cluster services.

## Ingredients

### Ingress controller

An _Ingress controller_ is the actual implementor of the ingress abstraction, here the chef has selected for you one of the finest controllers available: the [NGINX Ingress Controller](nginx-ingress/README.md)

### Certificate manager

The _certificate manager_ is an optional component that will cater to all your TLS certificate issuance desires in an automatic and standardized way.

Despite being fit also to in-cluster traffic, this component is mostly useful for securing Ingress resources.

The chef recommends the [Jetstack Cert-Manager](cert-manager/README.md) to accompany the main dish.
