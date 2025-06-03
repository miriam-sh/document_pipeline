import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="document_pipeline",
        user="postgres",
        password="n,fb,,gk",
        host="db",
        port="5432"
    )
