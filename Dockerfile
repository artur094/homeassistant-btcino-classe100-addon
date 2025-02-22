ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3

WORKDIR /app
COPY . /app/

RUN chmod +x /app/run.sh

RUN pip install -r requirements.txt

CMD ["./run.sh"]