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
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol
# สร้าง dir ตามนี้ /vol/web/media (ซึ่งเราจะสร้างทั้ง edia และ static folder) เพ่ืื่อใช้ในการเก็บ files
# -p เพื่อให้มันสร้าง subdirectories ที่เรากำหนดใน path (ประมาณว่าถ้า subdir ใหนไม่มีก็จะสร้างให้เลย)
# mkdir = make a directory

# กำหนด ownership ให้กับ /vol
# c h own รวมกันเป็น chown หรือ change owner
# -R คือ recursive ใส่เพื่อบอกว่าเราจะ change owner directory ทั้ง subdirectories ที่ slash มาด้วย
# แล้วกำหนด owoer ไปที่ django-user และ :django-user คือ group django-user แต่จะทำให้ user คนนี้สามารถเปลี่ยนแปลง dir นี้ได้ต้องกำหนด chmod -R 755

# chmod = Change mode คือเราจะทำการเปลี่ยนที่ /vol directory นี้ change permissions ที่ directory
# 755 หมายความว่า owner of that directory และ the group of that directory สามารถที่จะสร้าง chnage ที่ directory นี้ได้หมด หรือ files ใน directory นี้

# เราจะสร้าง dir ในการเก็บ files หลังจากสร้าง user เพื่อที่จะได้กำหนดให้ user ชื่อ django-user ให้สามารถเข้าถึง dir นั้นได้ (เพื่อทำเรื่อง permission)
# ถ้าเราไม่ทำแบบนี้เราก็จะไม่สามารถเข้าถึง folder นั้นได้ มันจะมีแค่ root user ที่เข้าถึงได้ซะงั้น

# apk add --update --no-cache postgresql-client jpeg-dev && \ # เป็น packages ที่ต้องอยู่หลังจาก build เสร็จ
# packages พวกนี้ต้อง install ใน docker image เพื่อรัน pillows
# จึงเป็น packages ที่ต้องอยู่ใน image ตลอดหลังจากเรา build image เสร็จ

# apk add --update --no-cache --virtual .tmp-build-deps \ # เป็น packages ที่จะลบหลังจาก ออกที่จะ build เสร็จ
    # build-base postgresql-dev musl-dev zlib zlib-dev && \
# ส่วน packages ที่ install ตรงนี้คือ เป็น package ที่เอาไว้เพื่อทำการ install pillar library เท่านั้น คือ zlib zlib-dev ซึ่งเราจะลบมันหลังจากเข้า build steps เพื่อให้ docker นั้น small and concise

ENV PATH="/py/bin:$PATH"

USER django-user