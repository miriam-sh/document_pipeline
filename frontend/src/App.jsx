import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');
  const [docId, setDocId] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("יש לבחור קובץ");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    setStatus("מעלה קובץ...");

    try {
      const res = await axios.post("http://localhost:3000/upload", formData);
      const { document_id } = res.data;
      setDocId(document_id);
      setStatus("קובץ הועלה. מזהה: " + document_id);
    } catch (err) {
      console.error(err);
      setStatus("שגיאה בהעלאה");
    }

    setUploading(false);
  };

  // Polling לסטטוס
  useEffect(() => {
    if (!docId) return;

    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`http://localhost:3000/status/${docId}`);
        const { status } = res.data;
        setStatus(`סטטוס: ${status}`);

        if (status === "completed" || status === "failed") {
          clearInterval(interval);
        }
      } catch (err) {
        console.error(err);
        setStatus("שגיאה בבדיקת סטטוס");
      }
    }, 3000); // כל 3 שניות

    return () => clearInterval(interval);
  }, [docId]);

  return (
    <div style={{ padding: 20, direction: 'rtl', fontFamily: 'sans-serif' }}>
      <h1>העלאת קובץ Excel</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={uploading}>העלה</button>
      <p>{status}</p>
    </div>
  );
}

export default App;
