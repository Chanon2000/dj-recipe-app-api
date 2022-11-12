#!/bin/sh
# ตรงนี้เรียกว่า shebang เพื่อ mock file นี้ว่าเป็น shell script file

set -e
# เพื่อบอกว่าเมื่อรัน command ด้านล่างนี้ ถ้า command ใหน fail มันจะ fail ทั้ง script

# command เพื่อ start server
python manage.py wait_for_db # ต้องรัน wait_for_db ก่อนแน่นอน เพราะ database ต้องพร้อมก่อน
python manage.py collectstatic --noinput # เพื่อ collect static แล้วใส่ใน dir ที่เรากำหนด ซึ่งเราจะทำให้ nginx เข้าถึง dirนั้นเพื่อ serve ในอนาคต (ไม่ส่งผ่าน django)
python manage.py migrate # เพื่อให้มันรัน migration เพื่อเรา start app

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
# ทำการรัน whiskey service คือ name ของ application we're running
# ผ่านเข้า socket 9000 ซึ่งรันมันบน TCP socket on Port 9000 โดย port นี้จะใช้โดย nginx server เพื่อ connect app

# --workers 4 จะมี whiskey workers ที่แตกต่างกัน นั้นคือ application ของเราจะ running บน 4 workers
# เราสามารถเปลี่ยนแปลงมันได้ขึ้นกับ จำนวน CPU ที่เรามี หรือที่ server เรา ซึ่งในที่นี้ 4 worker ถือเป็นตัวเลขที่ดี

# --master คือเราต้องการจะ set uwsgi demon หรือคือ running application เป็น master thread

# --enable-threads นั้นคือถ้าเราใช้ any multi-threading ใน application ของเรา เราสามารถใช้มันผ่าน whiskey service ได้

# --module app.wsgi เพื่อบอกว่าเราจะรัน wsgi.py file ใน app folder
# ซึ่ง Whiskey Service ใช้ wsgi.py file นั้นเป็น entry point ของ project
# app.wsgi เพราะ ชื่อ project ชื่อ app และไม่ต้องเติม .py เพราะมันวันจะรู้อยู่แล้ว