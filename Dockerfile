FROM python:alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

CMD gunicorn app:app --error-logfile gunicorn_error.log -b 0.0.0.0:8080 --thread 5
