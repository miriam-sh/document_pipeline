const cors = require("cors")
const express = require("express");
const multer = require("multer");
const path = require("path");
const { v4: uuidv4 } = require("uuid");
const { Pool } = require("pg");

const app = express();
const PORT = process.env.PORT || 3000;

const pool = new Pool({
    host: "db",
    user: "postgres",
    password: "doc_pipe",
    database: "document_pipeline",
    port: 5432,
});

// הגדרת אחסון קובץ
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, path.join(__dirname, "..", "uploads"));
    },
    filename: function (req, file, cb) {
        const uniqueName = uuidv4() + path.extname(file.originalname);
        cb(null, uniqueName);
    },
});

const upload = multer({ storage });

app.use(express.json());

app.use(cors())

app.post("/upload", upload.single("file"), async (req, res) => {
    const file = req.file;

    if (!file) {
        return res.status(400).json({ error: "No file uploaded." });
    }

    try {
        const result = await pool.query(
            `INSERT INTO documents (filename, status) VALUES ($1, $2) RETURNING id`,
            [file.filename, "uploaded"]
        );

        const documentId = result.rows[0].id;

        res.status(200).json({ message: "File uploaded", document_id: documentId });
    } catch (error) {
        console.error("Database error:", error);
        res.status(500).json({ error: "Database error" });
    }
});

app.get("/status/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const result = await pool.query(
            "SELECT status FROM documents WHERE id = $1",
            [id]
        );

        if (result.rowCount === 0) {
            return res.status(404).json({ error: "Document not found" });
        }

        res.json({ id, status: result.rows[0].status });
    } catch (error) {
        console.error("Error fetching status:", error);
        res.status(500).json({ error: "Database error" });
    }
});


app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
