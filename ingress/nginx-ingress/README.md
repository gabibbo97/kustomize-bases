# NGINX-INGRESS

The [NGINX Ingress](https://github.com/kubernetes/ingress-nginx) is a feature rich ingress controller maintained by the Kubernetes community as a reference implementation.

## Main course

It can be found in the `base` directory: it contains a minimal install of an NGINX Ingress controller, leveraging a `LoadBalancer` to be exposed.

## Toppings

### example-daemonset

If you're installing on shared hosting VPSs or facilities where you do not have access to a LoadBalacer, this patchset deploys multiple ingress controllers (one for each node) and exposes them on port 80 and 443, as if it were installed on the node itself.

### example-loadbalancer-ip

If you're installing on a baremetal environment and prefer to allocate a known loadbalancer IP this example shows you how to set it.
