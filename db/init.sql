CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'
);

CREATE TABLE extracted_data (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    item_name TEXT,
    item_value TEXT
);
