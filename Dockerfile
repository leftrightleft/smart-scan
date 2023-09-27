FROM python:3.10

COPY . /
RUN pip install -r requirements.txt
RUN pwd
# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]