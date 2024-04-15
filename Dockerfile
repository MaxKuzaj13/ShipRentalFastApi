FROM python:3.12-alpine

RUN mkdir /app

COPY ./src /app

RUN ls /app

RUN apk update && \
    apk add --no-cache postgresql-client

ENV PYTHONPATH=${PYTHONPATH}:/app


RUN pip install -r ./app/requirements.txt


WORKDIR /src

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
