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
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
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

# apk add --update --no-cache postgresql-client jpeg-dev && \ # เป็น packages ที่ต้องอยู่หลังจาก build เสร็จ
# packages พวกนี้ต้อง install ใน docker image เพื่อรัน pillows
# จึงเป็น packages ที่ต้องอยู่ใน image ตลอดหลังจากเรา build image เสร็จ

# apk add --update --no-cache --virtual .tmp-build-deps \ # เป็น packages ที่จะลบหลังจาก ออกที่จะ build เสร็จ
    # build-base postgresql-dev musl-dev zlib zlib-dev && \
# ส่วน packages ที่ install ตรงนี้คือ เป็น package ที่เอาไว้เพื่อทำการ install pillar library เท่านั้น คือ zlib zlib-dev ซึ่งเราจะลบมันหลังจากเข้า build steps เพื่อให้ docker นั้น small and concise

ENV PATH="/py/bin:$PATH"

USER django-user