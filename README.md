# rhasspy-tag-action

A Github Action to automatically tag a commit whenever the semper version in the file VERSION gets incremented

### Usage

```Dockerfile
name: Bump version
on:
  push:
    branches:
      - master
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Bump version and push tag
      uses: rhasspy/rhasspy-tag-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      id: bump_tag
    - name: update packages
      if: steps.bump_tag.outputs.new_tag
      run: <package-new-version-and-deploy>
```

#### Options

**Environment Variables**

* **GITHUB_TOKEN** ***(required)*** - Required for permission to tag the repo.

#### Outputs
outputs:
- **new_tag** - The new tag (only set when a new tag is added)
- **current_version** - The latest version after running this action

> ***Note:*** This action creates a [lightweight tag](https://developer.github.com/v3/git/refs/#create-a-reference).

### Workflow

* Add this action to your repo
* Commit some changes
* When the version in VERSION gets incremented, the action will push an updated tag to github
