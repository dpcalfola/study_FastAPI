FROM python:3.11.0rc2-alpine3.16

MAINTAINER FolaFlor
LABEL maintainer="https://dpcalfola.tistory.com/"

ENV PYTHONUNBUFFRED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./FastAPI_app /FastAPI_app
WORKDIR /FastAPI_app
EXPOSE 42187


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Install psycopg2 dependency applications
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    #
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    #
    adduser \
        --disabled-password \
        --no-create-home \
        FastAPI-user

ENV PATH="/py/bin:$PATH"

USER FastAPI-user