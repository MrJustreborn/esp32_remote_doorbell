#WSS
import asyncio
import pathlib
import ssl
import websockets

#db
from database import db_test_connect, db_get_user_by_esp_key, db_update_message_key_for_user, db_get_user_by_user_key

#REST
from flask import Flask
import _thread

import signal
import sys

USERS = {}

#WSS
async def register(websocket, path):
    USERS[path] = websocket
    print("register", str(path))

async def unregister(websocket, path):
    del USERS[path]
    print("unregister", str(path))

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