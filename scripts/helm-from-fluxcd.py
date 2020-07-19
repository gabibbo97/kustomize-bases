#!/usr/bin/env python3
# Install the provided helm.fluxcd.io/v1 HelmRelease
import yaml
import sys
import subprocess
import tempfile

# Parse CRDs from stdin
stdin = sys.stdin.read()
helm_release_crds = []
for obj in yaml.safe_load_all(stdin):
  # Check for fields
  if 'apiVersion' not in obj:
    continue
  if 'kind' not in obj:
    continue
  # Check for HelmReleases
  if obj.get('apiVersion') != 'helm.fluxcd.io/v1':
    continue
  if obj.get('kind') != 'HelmRelease':
    continue
  helm_release_crds.append(obj)

print(f'Found {len(helm_release_crds)} HelmRelease CRDs')

# Perform chart installations
def get_stdout_lines(process):
  return str(subprocess.run(process, stdout = subprocess.PIPE).stdout, 'UTF-8').splitlines()

def get_helm_repos():
  lines = get_stdout_lines(['helm', 'repo', 'list'])[1:]
  return map(lambda line : (line.split()[0], line.split()[1]), lines)

def install_helm_release_git(helm_release):
  name = helm_release['metadata']['name']
  namespace = helm_release['metadata'].get('namespace','default')
  # Clone git repo
  with tempfile.TemporaryDirectory() as tempdir:
    repo_url = helm_release['spec']['chart']['git']
    repo_ref = helm_release['spec']['chart']['ref']
    subprocess.run(['git', 'clone', '--depth=1', '-b', repo_ref, repo_url, tempdir])
    helm_chart_path = f"{tempdir}/{helm_release['spec']['chart']['path']}"
    # Extract values
    helm_chart_values = helm_release['spec'].get('values', {})
    # Install Helm repo
    with tempfile.NamedTemporaryFile('w') as temp:
      yaml.safe_dump(helm_chart_values, temp)
      subprocess.run(['helm', 'upgrade', name, helm_chart_path, '--namespace', namespace,
        '--atomic', '--cleanup-on-fail', '--create-namespace',
        '--install',
        '--reset-values',
        '--values', temp.name,
        '--wait'
      ])
    print('Chart installed')

def install_helm_release_repo(helm_release):
  name = helm_release['metadata']['name']
  namespace = helm_release['metadata'].get('namespace','default')
  # Converge Helm repo
  helm_repo_url = helm_release['spec']['chart']['repository']
  if not any([ x[1] == helm_repo_url for x in get_helm_repos() ]):
    helm_repo_name = input(f'Name for chart repository with URL {helm_repo_url}: ')
    subprocess.run(['helm', 'repo', 'add', helm_repo_name, helm_repo_url])
    subprocess.run(['helm', 'repo', 'update'])
  helm_repo_name = next(filter(lambda x : x[1] == helm_repo_url, get_helm_repos()))[0]
  # Search chart
  helm_chart_name = helm_release['spec']['chart']['name']
  helm_chart_full_name = f'{helm_repo_name}/{helm_chart_name}'
  helm_chart_version = helm_release['spec']['chart']['version']
  search_results = get_stdout_lines(['helm', 'search', 'repo', helm_chart_full_name])[1:]
  if not any([ helm_chart_version in x for x in search_results ]):
    subprocess.run(['helm', 'repo', 'update'])
  print(f'Found chart {helm_chart_full_name} {helm_chart_version}')
  # Extract values
  helm_chart_values = helm_release['spec'].get('values', {})
  # Install Helm repo
  with tempfile.NamedTemporaryFile('w') as temp:
    yaml.safe_dump(helm_chart_values, temp)
    subprocess.run(['helm', 'upgrade', name, helm_chart_full_name, '--namespace', namespace,
      '--atomic', '--cleanup-on-fail', '--create-namespace',
      '--install',
      '--reset-values',
      '--values', temp.name,
      '--version', helm_chart_version,
      '--wait'
    ])
  print('Chart installed')


for helm_release in helm_release_crds:
  name = helm_release['metadata']['name']
  namespace = helm_release['metadata'].get('namespace','default')
  # Skip non RepoChartSource charts
  if 'git' in helm_release['spec']['chart']:
    install_helm_release_git(helm_release)
  elif 'repository' in helm_release['spec']['chart']:
    install_helm_release_repo(helm_release)
