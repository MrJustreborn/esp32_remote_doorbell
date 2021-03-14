#WSS
import asyncio
import pathlib
import ssl
import websockets

#db
from database import db_test_connect, db_get_user_by_esp_key, db_update_message_key_for_user, db_get_user_by_user_key

#REST
from flask import Flask, Response, jsonify
import _thread

import signal
import sys

#firebase
import firebase_admin
from firebase_admin import credentials, messaging

#visitors
import time

cred = credentials.Certificate("remotedoorbell-cred.json")
frirebase_app = firebase_admin.initialize_app(cred)

USERS = {}

VISITORS_MODE = {}

#WSS
async def register(websocket, path):
    USERS[path] = websocket
    print("register", str(path))

async def unregister(websocket, path):
    if USERS[path].closed:
        del USERS[path]
        print("unregister", str(path))
    else:
        print("Cannot unregister, connection is still open for", str(path))

async def wss(websocket, path):
    esp = path[1:]
    print("WSS-Request: ", esp)
    user = db_get_user_by_esp_key(esp)
    if user is None:
        return

    await register(websocket, esp)
    try:
        await websocket.send("Hello")
        async for m in websocket:
            await _sendNotification(esp, m)
            print(esp, m)
    finally:
        await unregister(websocket, esp)

#REST
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"
@app.route('/open/<apiKey>', methods=['POST'])
def openDoor(apiKey):
    print(apiKey)
    user = db_get_user_by_user_key(apiKey)
    asyncio.set_event_loop(asyncio.new_event_loop())
    return asyncio.get_event_loop().run_until_complete(_openDoor(user))
@app.route('/setToken/<apiKey>/<token>', methods=['PUT'])
def setToken(apiKey, token):
    print(apiKey, token)
    resp = Response("Foo bar baz")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'text'
    print("Updated token:", db_update_message_key_for_user(token, apiKey))
    return resp
@app.route('/getUser/<apiKey>', methods=['GET'])
def getUser(apiKey):
    user = db_get_user_by_user_key(apiKey)
    if user is not None:
        return jsonify(user.getJson())
    return None
@app.route('/visitors/<apiKey>/<duration>', methods=['POST'])
def activateVisitosMode(apiKey, duration):
    user = db_get_user_by_user_key(apiKey)
    if user is None:
        return "0"
    VISITORS_MODE[apiKey] = {
        "start":time.time(),
        "duration":float(duration)*60
        }
    return {"timeleft":float(duration)*60, "duration":float(duration)*60}
@app.route('/visitors/<apiKey>', methods=['GET'])
def getVisitorsModeTimeLeft(apiKey):
    user = db_get_user_by_user_key(apiKey)
    if user is None:
        return {"timeleft":0, "duration":0}
    if apiKey in VISITORS_MODE:
        print(VISITORS_MODE[apiKey])
        timeLeft = VISITORS_MODE[apiKey]['start'] + VISITORS_MODE[apiKey]['duration'] - time.time()
        if timeLeft <= 0:
            del VISITORS_MODE[apiKey]
        return {"timeleft":int(timeLeft), "duration":int(VISITORS_MODE[apiKey]['duration'])}
    return {"timeleft":0, "duration":0}

#Helper
async def _openDoor(user):
    if user is not None:
        if user.esp_key in USERS:
            await USERS[user.esp_key].send("open")
            return "ok"
        else:
            print("No ESP registered")
            return "No ESP registered"
    else:
        return "foo"

async def _sendNotification(esp, what):
    await _visitorMode(esp, what)
    u = db_get_user_by_esp_key(esp)
    
    if u is None:
        return
    
    message = messaging.Message(
        notification=messaging.Notification(
            title="Suprise Motherfucker",
            body=what
        ),
        android=messaging.AndroidConfig(
            priority='high',
            notification=messaging.AndroidNotification(
                icon='icon',
                color='#f45342'
            )
        ),
        token=u.message_token
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)

async def _visitorMode(esp, what): #TODO: only open door if downstairs ring
    u = db_get_user_by_esp_key(esp)
    
    if u is None:
        print("No user found for visitorMode")
        return
    
    if u.user_key in VISITORS_MODE:
        timeLeft = VISITORS_MODE[u.user_key]['start'] + VISITORS_MODE[u.user_key]['duration'] - time.time()
        print("VisitorMode active: ", timeLeft)
        if timeLeft <= 0:
            del VISITORS_MODE[u.user_key]
        else:
            await _openDoor(u)

def flaskThread():
    app.run(debug=False, port=5000, host='0.0.0.0')

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    asyncio.get_event_loop().stop()
    sys.exit(0)

if __name__ == "__main__":
    #DB
    db_test_connect()

    #REST
    _thread.start_new_thread(flaskThread, ())

    #WSS
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
    localhost_key = pathlib.Path(__file__).with_name("key.pem")
    ssl_context.load_cert_chain(localhost_pem, keyfile=localhost_key)

    start_server = websockets.serve(
        wss, "*", 8765, ssl=None
    )

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()