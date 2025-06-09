import time
import subprocess

import psycopg2
from db_config import get_connection

def get_next_document():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, filename FROM documents
        WHERE status = 'uploaded'
        ORDER BY upload_time ASC
        LIMIT 1;
    """)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def mark_as_processing(doc_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE documents SET status = 'processing' WHERE id = %s", (doc_id,))
    conn.commit()
    cursor.close()
    conn.close()

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",
                dbname="document_pipeline",
                user="postgres",
                password="doc_pipe"
            )
            conn.close()
            print("Database is ready!")
            break
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(2)

def main_loop():
    wait_for_db()
    print("Watcher התחיל לפעול...")
    while True:
        doc = get_next_document()
        if doc:
            doc_id, filename = doc
            print(f"נמצא קובץ חדש לעיבוד: {filename} (ID={doc_id})")
            mark_as_processing(doc_id)
            subprocess.run(["python", "process_document.py", str(doc_id), filename])
        else:
            print("אין קבצים חדשים. ממתין 5 שניות...")
            time.sleep(5)

if __name__ == "__main__":
    main_loop()
