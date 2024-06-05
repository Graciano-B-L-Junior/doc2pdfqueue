
import os
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(host=os.environ.get('DB_HOST'),
                            user=os.environ.get('DB_USER'),
                            password=os.environ.get('DB_PASSWD'),
                            database=os.environ.get('DB')
                            )
    return conn


def register_user(login,passwd):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (login,password)
            values (%s, %s)
        """,(login,passwd))

        conn.commit()
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as err:
        print("#"*250)
        print(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return False

def get_user(login,passwd):
    uid=None
    name=None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, login FROM users
            WHERE login = %s AND password = %s
        """,(login,passwd))

        result = cursor.fetchone()
        uid, name = result
        

        cursor.close()
        conn.close()
    except Exception as err:
        print(err)
    finally:
        return (uid,name)