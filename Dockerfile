FROM python:3.10

RUN mkdir /async-python-sprint-4

WORKDIR /async-python-sprint-4

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x app_start.sh