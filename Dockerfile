FROM python:3.9-alpine3.13

LABEL maintainer="chanon2000"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
# โดยจะเป็น script ที่รันโดย docker application
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts
    # chmod -R +x /scripts เพื่อให้มั้นใจว่า scripts directory is executable เพราะเราต้อง execute scripts files นี้ใน directory นี้

# linux-headers package จำเป็นต่อ uWSGI server installation ซึ่งเมื่อ install uWSGI ก็ลบทิ้งได้เลย เพื่อให้ docker image นั้น lightweight

ENV PATH="/scripts:/py/bin:$PATH"
# เราต้องเพิ่ม path ของ scripts เข้าไป ไม่ทำก็รันไม่ได้

USER django-user

CMD ["run.sh"]
# run จะเป็นชื่อของ scripts ที่เราสร้าง แล้วทำการ execute file แบบนี้แหละ
# เราจะรัน command นี้ใน production แต่ใน dev เราจะ override มันใน docker-compose เพราะใน dev เราจะรัน manage.py runserver แทน