# Document Pipeline Project

This is an **end-to-end document processing pipeline** that allows users to upload a `.csv` file and analyze it based on **key-value** structure.

The project is composed of multiple components (backend, Python worker, frontend, and database), all **packaged with Docker** for easy setup and execution.

---

## Features

- Upload and parse `.csv` documents
- Store metadata in PostgreSQL
- Asynchronous processing using a Python worker
- Frontend interface for upload and result display
- Fully containerized with Docker and Docker Compose

---

## Getting Started

To run the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/miriam-sh/document_pipeline.git
   cd document_pipeline

2. Run the project with Docker:
   ```bash
    docker-compose up --build

3. Open your browser and go to: http://localhost:5173

---

## notes

Make sure Docker and Docker Compose are installed on your machine.
