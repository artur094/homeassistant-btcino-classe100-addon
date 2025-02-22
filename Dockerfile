ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3.12

RUN apk add --update py-pip

WORKDIR /app
COPY . /app/

RUN chmod +x /app/run.sh

RUN pip install -r requirements.txt --break-system-packages

CMD ["./run.sh"]