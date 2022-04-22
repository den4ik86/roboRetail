import pickle
from sqlalchemy import create_engine, insert, select, update, delete
from typing import Any, Dict
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import ujson
import socket
import sqlite3

app = FastAPI()

html ="""

<html>
  <head>
    <title>setup shelf</title>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  </head>
  <body>
   IP: <div id="ip"></div>
   id: <div id="id"></div>
   number: <div id="number"></div>
   url: <div id="url"></div>
   <span>All Weigth: <div id="weigth"></div></span>
<hr>
<form name='cf1'>
  sensor1 calibration factor:
   <input type="range" name="cf1" min='-20' max='20' step='0.05' value='0' id="r1" oninput="fun1()" onclick="sendChange1()" style="width:100%;">
   <p id="one"></p>
   <p>weigth sensor1: <div id="unit1"></div></p>
</form>
<hr>

<form name='cf2'>
  sensor2 calibration factor;
   <input type="range" name="cf2" min='-20' max='20' step='0.05' value='0' id="r2" oninput="fun2()" onclick="sendChange2()" style="width:100%;">
   <p id="two"></p>
   <p>weigth sensor2: <div id="unit2"></div></p>
</form>
<hr>

<form name='cf3'>
  sensor3 calibration factor;
   <input type="range" name="cf3" min='-20' max='20' step='0.05' value='0' id="r3" oninput="fun3()" onclick="sendChange3()" style="width:100%;">
   <p id="three"></p>
   <p>weigth sensor3: <div id="unit3"></div></p>
</form>
<hr>

<form name='cf4'>
  sensor4 calibration factor;
   <input type="range" name="cf4" min='-20' max='20' step='0.05' value='0' id="r4" oninput="fun4()" onclick="sendChange4()" style="width:100%;">
   <p id="four"></p>
   <p>weigth sensor4:</td> <div id="unit4"></div></p>
</form>

<form name='ur1'>
url:
<input type="url" name="url" value="">
id:
<input type="number" name="id" value="">
number:
<input tupe="number" name="number" value="">

<input type='submit' value="send & save" onclick="urlSender()">
</form>

<!--//////////////////////////////////////////////////// -->
<script>
 function fun1() {
    var rng=document.getElementById('r1');
    var p=document.getElementById('one');
    p.innerHTML=rng.value;
 }
 function fun2() {
    var rng=document.getElementById('r2');
    var p=document.getElementById('two');
    p.innerHTML=rng.value;
 }
 function fun3() {
    var rng=document.getElementById('r3');
    var p=document.getElementById('three');
    p.innerHTML=rng.value;
 }
 function fun4() {
    var rng=document.getElementById('r4');
    var p=document.getElementById('four');
    p.innerHTML=rng.value;
 }
////////////////////////////////////////////////////////////////////////////////
 function sendChange1(){
    let formData = new FormData(document.forms.cf1);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://78.140.57.122:61221/cf1');
    xhr.send(formData);
//    xhr.onload = () => alert(xhr.response);
 }

 function sendChange2(){
    let formData = new FormData(document.forms.cf2);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://78.140.57.122:61221/cf2');
    xhr.send(formData);
//    xhr.onload = () => alert(xhr.response);
 }

 function sendChange3(){
    let formData = new FormData(document.forms.cf3);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://78.140.57.122:61221/cf3');
    xhr.send(formData);
//    xhr.onload = () => alert(xhr.response);
 }

 function sendChange4(){
    let formData = new FormData(document.forms.cf4);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://78.140.57.122:61221/cf4');
    xhr.send(formData);
//    xhr.onload = () => alert(xhr.response);
 }

 function urlSender(){
    let formData = new FormData(document.forms.ur1);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://78.140.57.122:61221/url');
    xhr.send(formData);
//    xhr.onload = () => alert(xhr.response);
 }

////////////////////////////////////////////////////////////////////////////////

show();
setInterval(show, 1000);
function show(){
         let xhr = new XMLHttpRequest();
         xhr.open('GET', 'http://78.140.57.122:61221/client', false);
         xhr.send();
         if(xhr.status != 200){
            alert("Error connection");
         }else{
            let json;
            json = JSON.parse(xhr.responseText);
            document.getElementById("id").innerHTML = json["id"];
            document.getElementById("number").innerHTML = json["number"];
            document.getElementById("unit1").innerHTML = json["url"];
            document.getElementById("unit1").innerHTML = json["unit1"];
            document.getElementById("unit2").innerHTML = json["unit2"];
            document.getElementById("unit3").innerHTML = json["unit3"];
            document.getElementById("unit4").innerHTML = json["unit4"];
            document.getElementById("weigth").innerHTML= json["weigth"];
            document.getElementById("ip").innerHTML= json["ip"];

         }
}
</script>
</body>
</html>

"""
############################################################################

input = """
<!DOCTYPE html>
 <html>
  <body>
   <form id="input">
    User name:<br>
    <input type="text" name="name" value="">
    Password:<br>
    <input type="text" name="password" value="">
    <input type="submit" value="login">
   </form>
  </body>
 </html>
 <script>
   function submit(){
       let formData = new FormData(document.forms.input);
       let xhr = new XMLHttpRequest();
       xhr.open('POST', 'http://78.140.57.122:61221/input');
       xhr.send(formData);
//     xhr.onload = () => alert(xhr.response);

}
 </script>
"""

engine = create_engine('sqlite:///shelf.db')

@app.get('/')
async def get():
    return HTMLResponse(html)

#@app.post('/valid')
#async def valid(requet: Request, username: str = Form(...), password: str = Form(...)):
#    username 1f6503307f1eb3ea66a6be2c6ae4fae6
#    password 2a8277faa1cf6f3643d11055589e9073

#    devices = engine.execute("select * from shelf")
#    rows = devices.fetchall()



@app.get('/setup')
def setupMCU(request: Request):
    ip = request.client.host
    print (ip)
    result = engine.execute("select * from shelf where ip like :ip", ip)
    row = result.fetchall()
    if row != []:
        return row[0]
    else:
        defaultJsonMcu = {
                          "id": 0,
                          "number": 0,
                          "cf1": 1.8,
                          "cf2": 1.8,
                          "cf3": 1.8,
                          "cf4": 1.8,
                          "url": "",
                          }
    return defaultJsonMcu

@app.get('/service')
def getShelfValue(request: Request, id: int, number: int, cf1: float, cf2: float, cf3: float, cf4: float, unit1: float, unit2: float, unit3: float, unit4: float, weight: float, url: str):
    ip = request.client.host
    jsonData = {
                "id": id,
                "number": number,
                "cf1": cf1,
                "cf2": cf2,
                "cf3": cf3,
                "cf4": cf4,
                "unit1": unit1,
                "unit2": unit2,
                "unit3": unit3,
                "unit4": unit4,
                "weigth": weight,
                "url": url,
                "ip": ip,
                }
    file = open("tmp.json", "w")
    file.write(ujson.dumps(jsonData))
    file.close()

@app.get('/client')

def getUserRequest():
    response = ujson.load(open("tmp.json", "r"))
    return response

@app.get('/id')

def setId(request: Request, id: int):
    ip = request.client.host
    json = ujson.load(open("tmp.json", "r"))
    json['id'] = id
    file = open("tmp.json", "w")
    file.write(ujson.dumps(json))
    file.close()
    return json

@app.post('/number')
def setNum(request: Request, number: int = Form(...)):
    json = ujson.load(open("tmp.json", "r"))
    json['number'] = number
    file = open("tmp.json", "w")
    file.write(ujson.dumps(json))
    file.close()
    return json

@app.post('/cf1')

def setCf1(request: Request, cf1: float = Form(...)):
    json = ujson.load(open("tmp.json", "r"))
    json['cf1'] = cf1
    ip = json['ip']
    file = open("tmp.json", "w")
    file.write(ujson.dumps(json))
    file.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 80))
    sock.sendall(ujson.dumps(json).encode('utf-8'))
    sock.close()
    return json

@app.post('/cf2')
def setCf2(request: Request, cf2: float = Form(...)):
    json = ujson.load(open("tmp.json", "r"))
    json['cf2'] = cf2
    ip = json['ip']
    file = open("tmp.json", "w")
    file.write(ujson.dumps(json))
    file.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 80))
    sock.sendall(ujson.dumps(json).encode('utf-8'))
    sock.close()
    return json

@app.post('/cf3')
def setCf3(request: Request, cf3: float = Form(...)):
    json = ujson.load(open("tmp.json", "r"))
    json['cf3'] = cf3
    ip = json['ip']
    file = open("tmp.json", "w")
    file.write(ujson.dumps(json))
    file.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 80))
    sock.sendall(ujson.dumps(json).encode('utf-8'))
    sock.close()
    return json

@app.post('/cf4')
def setCf4(request: Request, cf4: float = Form(...)):
    json = ujson.load(open("tmp.json", "r"))
    json['cf4'] = cf4
    ip = json['ip']
    file = open("tmp.json", "w")
    file.write(ujson.dumps(json))
    file.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 80))
    sock.sendall(ujson.dumps(json).encode('utf-8'))
    sock.close()
    return json

@app.post('/url')
def setUrl(request: Request, id: int = Form(...), number: int = Form(...), url: str = Form(...)):
    json = ujson.load(open("tmp.json", "r"))
    json['url'] = url
    ip = json['ip']
    file = open("tmp.json", "w")
    file.write(ujson.dumps(json))
    file.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 80))
    sock.sendall(ujson.dumps(json).encode('utf-8'))
    sock.close()
    id = id
    number = number
    cf1 = json['cf1']
    cf2 = json['cf2']
    cf3 = json['cf3']
    cf4 = json['cf4']
    ip  = json['ip']
    url = json['url']
    engine.execute('insert into shelf (id, number, cf1, cf2, cf3, cf4, ip, url) values (:id, :number, :cf1, :cf2, :cf3, :cf4, :ip, :url)',id ,number, cf1, cf2, cf3, cf4, ip, url)
    return json

