import { useState } from "react";
import { uploadFile } from "../services/api";
import { scriptures } from "../data/scriptures";

function Upload() {
  const [file, setFile] = useState(null);
  const [scripture, setScripture] = useState("mahabharata");
  const [section, setSection] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("scripture", scripture);
    formData.append("section", section);

    try {
      await uploadFile(formData);
      alert("Upload successful!");
    } catch {
      alert("Upload failed");
    }
  };

  return (
    <div className="container">
      <div className="upload-card">
        <h2> Upload Scripture</h2>

        <select
          className="select"
          value={scripture}
          onChange={(e) => {
            setScripture(e.target.value);
            setSection("");
          }}
        >
          {Object.keys(scriptures).map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>

        <select
          className="select"
          value={section}
          onChange={(e) => setSection(e.target.value)}
        >
          <option value="">Select Section</option>
          {scriptures[scripture].map((sec) => (
            <option key={sec}>{sec}</option>
          ))}
        </select>

        <input type="file" onChange={(e) => setFile(e.target.files[0])} />

        <button onClick={handleUpload}>Upload</button>
      </div>
    </div>
  );
}

export default Upload;