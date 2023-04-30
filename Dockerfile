FROM python:3.10

WORKDIR /async-python-sprint-4

COPY requirements.txt .

RUN pip install -r requirements.txt && chmod 777 app_start.sh

COPY . .