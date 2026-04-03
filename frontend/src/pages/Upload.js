import { useState, useRef } from "react";
import { uploadFile } from "../services/api";
import { scriptures } from "../data/scriptures";
import axios from "axios";

function Upload() {
  //  ALL hooks must be inside component
  const [file, setFile] = useState(null);
  const [scripture, setScripture] = useState("mahabharata");
  const [section, setSection] = useState("");

  const [uploadStatus, setUploadStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const fileInputRef = useRef(null);

  const checkStatus = (fileId) => {
  const interval = setInterval(async () => {
    try {
      const res = await axios.get(
        `http://localhost:8000/api/status/${fileId}`
      );

      const status = res.data.status;

      if (status === "processing") {
        setUploadStatus(" Processing file...");
      }

      if (status === "completed") {
        setUploadStatus(" File processed successfully!");
        clearInterval(interval);
      }

      if (status === "failed") {
        setUploadStatus(" File processing failed!");
        clearInterval(interval);
      }

    } catch (err) {
      console.error(err);
      clearInterval(interval);
      setUploadStatus(" Error checking status");
    }
  }, 2000); // check every 2 sec
};

  const handleUpload = async () => {
  if (!file || !section) {
    setUploadStatus(" Please select file and section");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("scripture", scripture);
  formData.append("section", section);

  try {
    setLoading(true);
    setUploadStatus("⏳ Uploading file...");

    const res = await uploadFile(formData);

    const fileId = res.data.file_id;   // 🔥 get file_id

    setUploadStatus(" Processing file...");

//  START STATUS TRACKING
    checkStatus(fileId);

    setTimeout(() => {
  setUploadStatus(" File uploaded successfully!");
  setLoading(false);

  //  RESET FORM
  setFile(null);
  setSection("");
  fileInputRef.current.value = "";  //  CLEAR FILE INPUT

}, 2000);

  } catch (err) {
    console.error(err);

    if (err.response) {
      setUploadStatus(` ${err.response.data.detail}`);
    } else {
      setUploadStatus(" Server not reachable");
    }

    setLoading(false);
  }
};

  return (
    <div className="page">
      <div className="upload-box">

        <h2 className="title"> Upload Sacred Files</h2>

        <div className="dropdown-row">

          <select
            className="select large"
            value={scripture}
            onChange={(e) => {
              setScripture(e.target.value);
              setSection("");
            }}
          >
            {Object.keys(scriptures || {}).map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>

          <select
            className="select large"
            value={section}
            onChange={(e) => setSection(e.target.value)}
          >
            <option value="">Select Section</option>
            {scriptures[scripture]?.map((sec) => (
              <option key={sec} value={sec}>
                {sec}
              </option>
            ))}
          </select>

        </div>

        <input
  ref={fileInputRef}  
  type="file"
  className="file-input small"
  onChange={(e) => setFile(e.target.files[0])}
/>

        <button
          className="upload-btn"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "Uploading..." : "Upload"}
        </button>

        {/*  NOW USED → no warning */}
        {uploadStatus && (
          <p className="upload-status">{uploadStatus}</p>
        )}

      </div>
    </div>
  );
}

export default Upload;
