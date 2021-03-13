import asyncio
import pathlib
import ssl
import websockets

import psycopg2
from config import config

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name} - {path}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

def connect_db():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == "__main__":
    connect_db()
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
    localhost_key = pathlib.Path(__file__).with_name("key.pem")
    ssl_context.load_cert_chain(localhost_pem, keyfile=localhost_key)

    start_server = websockets.serve(
        hello, "*", 8765, ssl=ssl_context
    )

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()