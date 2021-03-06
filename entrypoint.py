from Version import Version
from pathlib import Path
import subprocess
from datetime import datetime
import os
import json
import requests

subprocess.run(['git', 'fetch', '--depth=1', 'origin', '+refs/tags/*:refs/tags/*'])
results = subprocess.run(['git', 'tag'], capture_output=True).stdout.decode().split()

version = max(Version.fromString(tag) for tag in results) if results else Version.fromString('')

# get current commit hash for tag
commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True).stdout.decode().strip()

with open('VERSION') as f:
    new_version_string = f.readline()

new_version = Version.fromString(new_version_string)

print(f'current version: {version}')
print(f'commit version: {new_version}')

if new_version > version:
    print(f'::set-output name=new_tag::v{new_version}')
    print(f'::set-output name=current_version::{new_version}')

    remote = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True).stdout.decode().strip()
    repo = Path(remote).stem

    timestampStr = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    full_name = os.environ['GITHUB_REPOSITORY']
    with open(os.environ['GITHUB_EVENT_PATH']) as f:
        github_event_json = json.load(f)

    git_refs_url = github_event_json['repository']['git_refs_url'].strip('"').replace('{/sha}', '')

    print(f'{timestampStr}: **pushing tag v{new_version} to repo {full_name}')

    result = requests.post(
        git_refs_url,
        json={
            "ref": f"refs/tags/v{new_version}",
            "sha": commit
        },
        headers={'Authorization': f'token {os.environ["GITHUB_TOKEN"]}'}
    )
else:
    print('The Version number in VERSION was not increased. Skipping...')
    print(f'::set-output name=current_version::{version}')
