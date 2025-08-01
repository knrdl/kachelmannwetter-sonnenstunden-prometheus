FROM python:3.13.5-alpine3.21

ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

RUN adduser --home /home/app --disabled-password --shell /bin/false --uid 1000 app

RUN pip install --no-cache-dir requests

CMD ["python3", "main.py"]

EXPOSE 8080/tcp

WORKDIR /app

RUN apk update --no-cache

USER app

COPY main.py metrics.py ./

