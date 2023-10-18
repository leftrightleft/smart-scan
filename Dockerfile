FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install -r /app/requirements.txt --target=/app 

ENV PYTHONPATH /app
CMD ["/app/src/smart_scan.py"]