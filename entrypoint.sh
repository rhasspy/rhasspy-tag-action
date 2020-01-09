#!/bin/bash

# fetch tags
git fetch --tags

# get latest tag
git fetch --tags
tagSha=$(git rev-list --tags --max-count=1)
if [ -z "$tagSha" ]
then
    version='0.0.0'
else
    tag=$(git describe --tags $tagSha)
	version="${tag:1}"
fi


# get current commit hash for tag
commit=$(git rev-parse HEAD)
new_version=$(head -1 VERSION)


if [[ $new_version > $version ]]
then
new_tag="v$new_version"

# set outputs
echo ::set-output name=new_tag::$new_tag
echo ::set-output name=current_version::$version

# get repo name from git
remote=$(git config --get remote.origin.url)
repo=$(basename $remote .git)

# push new tag ref to github
dt=$(date '+%Y-%m-%dT%H:%M:%SZ')
full_name=$GITHUB_REPOSITORY
git_refs_url=$(jq .repository.git_refs_url $GITHUB_EVENT_PATH | tr -d '"' | sed 's/{\/sha}//g')

echo "$dt: **pushing tag $new_tag to repo $full_name"

# POST a new ref to repo via Github API
curl -s -X POST $git_refs_url \
-H "Authorization: token $GITHUB_TOKEN" \
-d @- << EOF
{
  "ref": "refs/tags/$new_tag",
  "sha": "$commit"
}
EOF

else
    echo "The Version number in VERSION was not increased. Skipping..."
    echo ::set-output name=current_version::$version
fi
