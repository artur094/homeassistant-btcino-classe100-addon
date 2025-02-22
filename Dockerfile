FROM python:3.12

WORKDIR /app
COPY . /app

RUN chmod +x /app/run.sh

RUN pip install -r requirements.txt

CMD ["/app/run.sh"]