# Registry

The [registry](https://github.com/docker/distribution) is a component that allows storage of your container images.

## Main course

It can be found in the `base` directory: it contains a minimal install of the registry.

The dish is incomplete and you should utilize the `storage-filesystem` or `storage-s3` recipes, depending on your taste.

## Finishing touches

### storage-filesystem

Storage filesystem leverages a `PersistentVolumeClaim`, it is not HA and will not allow you to scale horizontally.

It's cool for personal clusters.

### storage-s3

This configuration leverages an external `S3-like` storage system.

It can be effortlessely scaled.

Chef's pick for _production_ workloads.

## Toppings

### ingress

This topping, applied on top of the previous bases allows to expose the registry, implementing authentication in the process.

Take a look at the [kustomization file](ingress/kustomization.yaml) to see how to add your own credentials.
