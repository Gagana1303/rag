import { BrowserRouter, Routes, Route } from "react-router-dom";
import Upload from "./pages/Upload";
import Chat from "./pages/Chat";
import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;