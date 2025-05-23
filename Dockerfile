FROM python:3.13.3-alpine3.20

ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

RUN adduser --home /home/app --disabled-password --shell /bin/false --uid 1000 app

CMD ["python3", "main.py"]

EXPOSE 8080/tcp

WORKDIR /app

RUN apk update --no-cache

USER app

COPY main.py metrics.py ./

