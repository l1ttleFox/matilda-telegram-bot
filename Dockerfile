FROM python:3.11

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

VOLUME /app/logs
VOLUME /app/db

COPY .env /app/.env
COPY src/ /app/

CMD python /app/main.py
