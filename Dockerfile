FROM python:3.9-alpine3.13 
# https://hub.docker.com/_/python
# python คือชื่อ image, 3.9-alpine3.13 คือชื่อ tag ที่จะใช้ เราใช้ Alpine version เพราะมันเป็น lightweight version of Linux มันมี dependencies ที่ไม่จำเป็น ไม่เยอะ ทำให้มันเบาและเหมาะต่อการรัน container

LABEL maintainer="chanon2000"
# เพื่อบอกว่าคนที่ลูแล Docker image นี้คือใคร ทำให้คนอื่นที่เข้ามาทำ project รู้ว่าใครเป็น maintainer
# ใส่เป็นชื่อ github หรืออะไรก็ได้ที่บอกว่าคือคุณ

ENV PYTHONUNBUFFERED 1
# ควรใส่ เมื่อรัน python บน docker container
# เพื่อบอก python ว่าไม่ต้อง buffer output ซึ่งจะทำให้ output จาก python ถูก print ลง console อย่างรวดเร็วแบบไม่มี delay

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# เอาทุก command ที่จะรัน มันทำใน RUN block นี้เลย
# เนื่องจาก docker จะสร้าง new image layer ในทุก command ที่เราทำใน dockerfile ดังนั้นเพื่อให้ image ดู lightweight เราเลยสั่ง RUN command แค่อันเดียว แล้วเขียนทำหลายๆ python command โดยใส่ \ เพื่อให้เขียนได้หลายๆบรรทัด
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --on-create-home \
        django-user
# เราทำการ RUN command ใน alpine image ที่เราใช้ในการ build image ของ project
# python -m venv /py เพื่อสร้าง virtual environment เพื่อเก็บ dependencies (ซึ่งจริงๆเราสามารถเก็บ python dependencies ที่ image base ได้แค่ในบาง case เก็บไว้ใน image เลยอาจทำให้ conflict กับ dependencies ใน project ได้ เพื่อลดความเสี่ยงก็เก็บลง vm เลยดีกว่า ซึ่งมันไม่ได้เพิ่มทรัพยากรมากนัก (ทำแบบนี้(vm)เพื่อ safeguards against any conflicting dependencies กับ base image))
# /py/bin/pip install --upgrade pip => เริ่มจาก full path จาก vm เข้า pip dir (ของ vm) แล้วทำการ upgrade PIP ใน vm
# /py/bin/pip install -r /tmp/requirements.txt => ทำการ install dependencies ต่างๆจาก requirements.txt 
# rm -rf /tmp => ลบ /tmp dir เพราะเราไม่ต้องการ extra dependencies on our image สร้างขึ้นมา เพื่อให้ docker image เรา lightweight เท่าที่จะทำได้

# ใน adduser block => ทำการ เพิ่่ม user ลง image เพื่อที่เราจะได้ไม่ต้องใช้ root user (ซึ่งมีอยู่ใน alpine image อยู่แล้ว) (root user คือ user that has the full access and permissions to do everything on the on the server)
# ไม่ควรรัน application โดยใช้ root user เพราะนั้นจะทำให้เมื่อ application ถูก hack ตัว attacker จะ full access to everything on that Docker ทันที
# ซึ่งถ้าเราสร้าง user ใหม่เพื่อทำการรัน ตัว attacker จะทำได้แค่ที่ user ที่สร้างมาทำได้ใน container นั้น (นี้คือเหตุผลที่เราทำการ add user ใหม่)
# --disabled-password เพราะเราไม่ต้องการใน people สามารถ login โดยใช้ password เข้า container (เพราะเราจะแค่ทำการรัน project เท่านั้นไม่ได้จะทำอย่างอื่นแล้ว)
# django-user => คือชื่อของ user ที่สร้างนั้นแหละ

# /py/bin/pip ใส่ path นี้จะหมายความว่าทำใน vm

ENV PATH="/py/bin:$PATH"
# ทำการ update PATH (คือ environment variable ที่ถูกสร้าง automatically โดย Linux operating systems) ใน image เพื่อใส่ path ที่จะ executables run command ต่างๆ (ซึ่งจะช่วยทำให้ทุกครั้งที่รันใน vm เราไม่ต้องกำหนด full path (/py/bin/pip) ของ app)
# ดังนั้นเมื่อเรารัน python command มันก็จะรันที่ vm เลย

USER django-user
# switch มาที่ django-user (หรือก็คือ user ที่เราพึงสามารถขึ้นมานี้แหละ)
# command ก่อนหน้านี้เราทำการรันโดย root user นะ แต่ต่อจากนี้จะรันด้วย django-user