FROM alpine
LABEL "repository"="https://github.com/maxbachmann/rhasspy-tag-action"
LABEL "homepage"="https://github.com/maxbachmann/rhasspy-tag-action"
LABEL "maintainer"="Max Bachmann"

COPY entrypoint.sh /entrypoint.sh

RUN apk update && apk add bash git curl jq

ENTRYPOINT ["/entrypoint.sh"]
