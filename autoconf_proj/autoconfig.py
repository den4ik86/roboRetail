from sqlalchemy import create_engine, insert, select, update, delete
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
import sqlite3
import ujson
import os

engine = create_engine('sqlite:///router.db')

app=FastAPI()

@app.get('/settings')
def getMac(mac: str):

    result= engine.execute('select * from devices where mac like :mac', mac)
    return result.fetchall()

@app.get('/admin')
def admin(id: int, mac: str, ip_vpn: str, ip_lan: str, ssid: str, pswd: str, srv_pub: str, srv_ip: str):

    f = open('ip', "w")
    f.write(ip_vpn)
    f = open('ip_lan', "w")
    f.write(ip_lan)
    os.system("wg genkey | tee client_private_key | wg pubkey > client_public_key")
    priv_key = open('client_private_key')
    pub_key  = open('client_public_key')

    priv_key = priv_key.read()
    pub_key  = pub_key.read()

    priv_key = priv_key.strip()
    pub_key  = pub_key.strip()

    engine.execute('insert into devices (id, mac, pub_key, priv_key, ip_vpn, ip_lan, ssid, pswd, srv_pub, srv_ip) values (:id, :mac, :pub_key, :priv_key, :ip_vpn, :ip_lan, :ssid, :pswd, :srv_pub, :srv_ip )',id ,mac , pub_key, priv_key, ip_vpn, ip_lan, ssid, pswd, srv_pub, srv_ip)
    return priv_key

html = """
<html>
 <body>
  <form action = "/admin" method = "GET">
   id
   <input type="text" name="id" value="">
   <br>
   MAC:
   <input type="text" name="mac" value="">
   <br>
   vpn_ip:
   <input type="text" name="ip_vpn" value="">
   <br>
   lan_sub_net (example: 192.168.80.0/24)<br>
   <input type="text" name="ip_lan" value="">
   <br>
   ssid wifi
   <input type="text" name="ssid" value="">
   <br>
   password
   <input type="text" name="pswd" value="">
   <input type="hidden" name = "srv_pub" value="rdN677Dwla8glivlPUpHXD3yAcgVlHlwc/CLB3gTUXA=">
   <input type="hidden" name = "srv_ip" value="10.10.10.1"
   <br>
   <input type="submit" value="send">
 </form>
 </body>
</html>

"""

@app.get('/')
async def get():
    return HTMLResponse(html)
