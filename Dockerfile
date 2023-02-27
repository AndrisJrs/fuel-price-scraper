FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV LOG_LEVEL="WARNING"

CMD ["python", "main.py"]