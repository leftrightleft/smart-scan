FROM python:3.10

# COPY smart-scan/ /github/workspace

# # RUN pip install requirements.txt
# RUN pwd
# RUN ls -al
# CMD ["python", "main.py"]

COPY COPY . /

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]