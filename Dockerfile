FROM python:3.9-alpine3.13 

LABEL maintainer="chanon2000"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# apk add --update --no-cache postgresql-client: install postgresql-client เป็น package ที่เราต้อง install ใน Alpine image เพื่อสำหรับ Psycopy2 ให้สามารถ connect กับ Postgres ได้ (postgresql-client คือ dependency ที่จำเป็นต้องอยู่ใน docker image เมื่อเรา running ใน production)

# apk add --update --no-cache --virtual .tmp-build-deps: ทำการกำหนด virtual dependency package เพื่อทำการ group packages ที่เรา install ลงใน .tmp-build-deps ซึ่ง package ที่ group ตรงนี้จะเป็น packages ที่จำเป็นเพื่อที่จะ install Postgres adapter (Psycopy2) นั้นก็คือ build-base, postgresql-dev, musl-dev # สรุป ทำการ install แล้ว list มันลงใน .tmp-build-deps

# apk del .tmp-build-deps && \: ทำการลบ package ที่อยู่ใน .tmp-build-deps นั้นก็คือ package ที่มีไว้เพื่อ install Psycopy2 ดังนั้นเมื่อ install เสร็จก็ลบทิ้งได้ เพื่อทำให้ image lightweight และ clean มากขึ้น
# ทำให้เรามีแต่ package ที่จำเป็นต่อ app แค่นั้น

ENV PATH="/py/bin:$PATH"

USER django-user