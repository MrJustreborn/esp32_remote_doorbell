#WSS
import asyncio
import pathlib
import ssl
import websockets

#db
from database import db_test_connect, db_get_user_by_esp_key, db_update_message_key_for_user

#REST
from flask import Flask
import _thread

import signal
import sys

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name} - {path}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

#REST
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

def flaskThread():
    app.run(debug=False, port=5000, host='0.0.0.0')

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    asyncio.get_event_loop().stop()
    sys.exit(0)

if __name__ == "__main__":
    #DB
    db_test_connect()
    user = db_get_user_by_esp_key("key_esp")
    print(user)
    print(db_update_message_key_for_user("TOKEN", "key"))


    #REST
    _thread.start_new_thread(flaskThread, ())

    #WSS
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
    localhost_key = pathlib.Path(__file__).with_name("key.pem")
    ssl_context.load_cert_chain(localhost_pem, keyfile=localhost_key)

    start_server = websockets.serve(
        hello, "*", 8765, ssl=ssl_context
    )

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()