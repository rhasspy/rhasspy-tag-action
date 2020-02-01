FROM python:slim-buster
LABEL "repository"="https://github.com/rhasspy/rhasspy-tag-action"
LABEL "homepage"="https://github.com/rhasspy/rhasspy-tag-action"
LABEL "maintainer"="Max Bachmann"

COPY entrypoint.py /entrypoint.py
COPY Version.py /Version.py

RUN pip3 install requests

ENTRYPOINT ["python3 /entrypoint.py"]
