import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="192.128.12.157",
        database="xacti",
        port="5432",
        user="postgres",
        password="postgres123" #juliusryanlistianto25
    )
    return conn

