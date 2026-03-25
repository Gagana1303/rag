import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

export const uploadFile = (data) => API.post("/api/upload", data);
export const askQuestion = (data) => API.post("/api/ask", data);