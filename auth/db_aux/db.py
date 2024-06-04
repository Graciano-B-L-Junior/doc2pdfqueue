
import os
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(host=os.environ.get('DB_HOST'),
                            database=os.environ.get('DB'),
                            user=os.environ.get('DB_USER'),
                            password=os.environ.get('DB_PASSWD'))
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
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return False