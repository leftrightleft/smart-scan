FROM python:3.10

COPY smart-scan/ .

# RUN pip install requirements.txt

RUN ls -al
CMD ["python", "./main.py"]