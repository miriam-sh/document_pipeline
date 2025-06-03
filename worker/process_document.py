import os
import sys
import pandas as pd
import base64
import xml.etree.ElementTree as ET
from db_config import get_connection

def decode_and_extract(file_path):
    df = pd.read_csv(file_path)

    def decode(row):
        if row['type'] == 'base64':
            try:
                decoded_bytes = base64.b64decode(row['content'])
                return decoded_bytes.decode('utf-8')
            except Exception:
                return None
        else:
            return row['content']

    df['decoded_content'] = df.apply(decode, axis=1)

    extracted = []

    for idx, content in enumerate(df['decoded_content']):
        try:
            if not content:
                continue
            root = ET.fromstring(content)
            for item in root.findall('item'):
                extracted.append({
                    "source_row": idx,
                    "item_name": item.attrib.get("name"),
                    "item_value": item.text
                })
        except Exception as e:
            print(f"שגיאה בשורה {idx}: {e}")

    return extracted


def save_extracted_data(document_id, extracted_items):
    conn = get_connection()
    cursor = conn.cursor()

    for item in extracted_items:
        cursor.execute("""
            INSERT INTO extracted_data (document_id, item_name, item_value)
            VALUES (%s, %s, %s)
        """, (document_id, item["item_name"], item["item_value"]))

    conn.commit()
    cursor.close()
    conn.close()


def update_status(document_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE documents SET status = %s WHERE id = %s", (new_status, document_id))
    conn.commit()
    cursor.close()
    conn.close()


def process_document(document_id, filename):
    try:
        path = os.path.join(os.path.dirname(__file__), "../uploads", filename)
        extracted = decode_and_extract(path)
        save_extracted_data(document_id, extracted)
        update_status(document_id, "completed")
        print(f"✅ מסמך {document_id} הושלם")
    except Exception as e:
        update_status(document_id, "failed")
        print(f"❌ שגיאה בעיבוד מסמך {document_id}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("שימוש: python process_document.py <document_id> <filename>")
        sys.exit(1)

    doc_id = int(sys.argv[1])
    filename = sys.argv[2]
    process_document(doc_id, filename)
