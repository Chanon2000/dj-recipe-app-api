# สร้าง dockerfile เพื่อรัน nginx เป็น service ของproject เรา บน docker

FROM nginxinc/nginx-unprivileged:1-alpine
# ใช้ base image
# nginxinc image: https://hub.docker.com/r/nginxinc/nginx-unprivileged
# เราใช้ nginx unprivileged instance ซึ่งก็มาจาก official nginx repo นั้นแหละ ซึ่งมันก็จะให้ unprivileged instance ของ nginx ซึ่งทำให้ app เรา secureมากขึ้น
# nginxinc ไม่จำเป็นต้องมี root user account เพราะมันจะทำแค่รันและให้เราเข้าถึง directory ที่ระบุ เพื่อที่เราจะได้สามารถจัดการ request จาก directory นั้นได้


# ถ้าเราใช้ nginx image ตรงๆ มันจะรันใน root mode user ซึ่งไม่ใช่เรื่องดีสำหรับ security เราต้องรัน application ใน least privileges (สิทธิ์) ให้น้อยที่สุด
# nginx image: https://hub.docker.com/_/nginx


LABEL maintainer="chanon2000"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
# copy มาเก็บลง docker image ซึ่งเป็น location ที่ nginx จะเข้ามาหา เมื่อมันพลายามจะ pull configuration
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh
# copy run.sh นั้นแหละ

ENV LISTEN_PORT=8000
# เป็น default variable สำหรับ container ซึ่งเป็น Environment variables ที่ running จาก image
# ซึ่งถ้าเราไม่กำหนด หรือ override ตรงนี้มันก็จะเป็น default value
ENV APP_HOST=app
# app คือ hostname ที่ Whiskey running
ENV APP_PORT=9000
# คือ port ที่ Whiskey app จะรัน

USER root
# กลับมาที่ root user ตรงนี้เพื่อทำการ setup image ด้านล่าง เพื่อรัน command ต่างๆ

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

# สร้าง /vol/static และกำหนด permission 755 ที่ /vol/static เพื่อที่เราจะสามารถอ่าน content ในนั้นได้
# สร้าง default.conf file เพราะเราจะกำหนด permission ให้กับ nginx user ทำการแก้ไขได้ เพราะเมื่อเรา execute run.sh file (ใน proxy folder) มันมี substitute command ซึ่งนั้นทำให้ user ของเราต้องมีสิทธิ์ในการเขียน file นั้นได้ เพื่อ override content
# ซึ่ง touch จะแค่สร้าง empty file ใน location ที่กำหนด ต่อมาก็ chown เพื่อให้สิทธิ nginx user (เป็น user ที่มาจาก base image)
# chmod เพื่อให้ docker container ของเราสามารถรัน run.sh ได้

VOLUME /vol/static
# ซึ่งจะเป็น default volume เพื่อสร้าง image ซึ่งในอนาคตเราจะ mapping volume นี้กับ docker-compose configuration

USER nginx
# switch กับมาที่ nginx user เพื่อไม่ให้รัน app โดยใช้ root user เพื่อจำกัดสิทธิการเข้าถึงให้น้อยลง

CMD ["/run.sh"]
# รัน run.sh ซึ่งเป็น default script เมื่อเราสร้าง instances จาก image นี้
# (หรือเรียกว่า "เรียก run.sh" แทนคำว่า "รัน run.sh")