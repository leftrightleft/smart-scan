FROM python:3.11-slim

COPY . /
RUN pip install -r requirements.txt

ENV PYTHONPATH /src

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]