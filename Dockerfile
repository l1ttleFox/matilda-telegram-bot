FROM python:3.11

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY .env /app/.env
COPY src/ /app/

CMD python /app/main.py
