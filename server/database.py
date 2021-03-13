#DB
import psycopg2
from config import config

class User:
    def __init__(self, id, name, user_key, message_token, esp_key):
        self.id = id
        self.name = name
        self.user_key = user_key
        self.message_token = message_token
        self.esp_key = esp_key
        print("Init new User")
    def __str__(self):
        return "User: " + str(self.id) + " - " + str(self.name)


def db_test_connect():
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

def db_get_user_by_esp_key(esp_key) -> User:
    return _db_get_user_by('esp_key', esp_key)
def db_get_user_by_message_token(token) -> User:
    return _db_get_user_by('message_token', token)
def db_get_user_by_user_key(user_key):
    return _db_get_user_by('user_key', user_key)

def db_update_message_key_for_user(token, user_key) -> bool:
    sql = """ UPDATE public.users
                SET message_token = %s
                WHERE user_key = %s"""
    conn = None
    updated_rows = 0
    
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (token, user_key))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows > 0


def _db_get_user_by(column, value):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.users WHERE " +column+ " = %s;", (value,))
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        u = None
        if row is not None:
            _id, name, user_key, message_token, esp_key = row
            u = User(_id, name, user_key, message_token, esp_key)

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
        
        if u is not None:
            return u
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()