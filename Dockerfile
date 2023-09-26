FROM python:3.10

COPY smart-scan/ .

# RUN pip install requirements.txt

CMD ["python", "./smart-scan/main.py"]