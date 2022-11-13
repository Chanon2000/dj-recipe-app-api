#!/bin/sh

set -e # เพื่อให้เมื่อมีบาง command ด้านล่างนี้ fail มันก็จะ fail ทั้ง file

# envsubst => environment substitute
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
# insert /etc/nginx/default.conf.tpl คือ file ที่เราสร้างนี้แหละ เข้าไปที่
    # โดยมันจะ substitute ทุก syntax ที่เป็น ${} ด้วย environment variable ที่ตรงกับชื่อของมัน แล้ว output ไปให้กับ location ที่กำหนด (กระบวนการทั้งหมดนี้เดียวเราจะทำให้ docker image)
# แล้ว output มาที่ /etc/nginx/conf.d/default.conf ซึ่งเป็น default configuration ของ nginx

# นี้คือวิธีการใส่ onfiguration values ให้กับ nginx ในช่วง runtime เมื่อคุณรัน server

nginx -g 'daemon off;' # มันจะ start nginx ด้วย configuration ที่เรากำหนด
# 'daemon off;' คือบอกว่าเราจะรัน nginx ใน foreground (หรือคือรันอยู่บนสุด หรือคือเป็น primary ในการรันบน Docker container) เพราะ เมื่อรัน nginx server มันจะ running ใน background และเราสามารถ interact มันผ่าน service manager เพราะทั้งหมดนี้เรารันใน Docker container
# ซึ่งจะทำให้ logs ต่างๆมัน output ออกมาที่หน้าจอ และ Docker container ก็จะรันเท่าที่ nginx รันอยู่ และถึงแม้ nginx ถูก kill นั้น Docker container ก็จะรันอยู่