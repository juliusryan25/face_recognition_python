import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="xacti",
        port="5432",
        user="postgres",
        password="sql123"
    )
    return conn

