FROM python:3.10

COPY smart-scan/ .

# RUN pip install requirements.txt

CMD ["python", "./main.py"]