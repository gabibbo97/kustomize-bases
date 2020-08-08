#!/bin/sh
set -e

# Add helm repo
helm repo list | grep -q 'fluxcd' || helm repo add fluxcd https://charts.fluxcd.io
helm repo update

ensureChart() {
  if ! helm search repo --versions "$1" | grep -q "$2"; then
    helm repo update
  fi
}

# Create SSH key
kubectl get namespace fluxcd || kubectl create namespace fluxcd
if ! kubectl -n fluxcd get secret fluxcd-ssh; then
  ssh-keygen -q -N "" -f ./identity
  kubectl -n fluxcd create secret generic fluxcd-ssh --from-file=./identity
  rm -f ./identity
  printf 'SSH KEY\n'
  cat ./identity.pub
  printf 'SSH KEY\n'
  printf 'Added? ' && read -r
  rm -f ./identity.pub
fi

# Install FluxCD
ensureChart fluxcd/flux v1.4.1
helm upgrade fluxcd fluxcd/flux \
  --atomic --cleanup-on-fail --create-namespace --install \
  --version v1.4.1 \
  --namespace fluxcd \
  --set git.url=git@gitlab.com:studio-longo/manifests.git \
  --set git.secretName=fluxcd-ssh \
  --set prometheus.enabled=true \
  --set manifestGeneration=true \
  --set syncGarbageCollection.enabled=true

ensureChart fluxcd/helm-operator 1.2.0
helm upgrade fluxcd-helm-operator fluxcd/helm-operator \
  --atomic --cleanup-on-fail --create-namespace --install \
  --version 1.2.0 \
  --namespace fluxcd \
  --set git.ssh.secretName=fluxcd-ssh \
  --set logReleaseDiffs=true \
  --set helm.versions=v3 \
  --set prometheus.enabled=true
