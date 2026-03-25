import { useState, useRef, useEffect } from "react";
import { askQuestion } from "../services/api";
import Sidebar from "../components/Sidebar";

function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const [scripture, setScripture] = useState("mahabharata");
  const [section, setSection] = useState("");

  const bottomRef = useRef();

  // 🔥 Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleAsk = async () => {
    if (!question) return;

    const updated = [...messages, { type: "user", text: question }];
    setMessages(updated);
    setQuestion("");
    setLoading(true);

    try {
      const res = await askQuestion({
        question,
        scripture,
        section
      });

      setMessages([
        ...updated,
        { type: "bot", text: res.data.answer }
      ]);
    } catch {
      setMessages([
        ...updated,
        { type: "bot", text: "Error fetching answer" }
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="chat-layout">

      {/* Sidebar */}
      <Sidebar
        scripture={scripture}
        setScripture={setScripture}
        section={section}
        setSection={setSection}
      />

      {/* Chat Area */}
      <div className="chat-area">

        <div className="messages">
          {messages.map((msg, i) => (
            <div key={i} className={`msg ${msg.type}`}>
              {msg.text}
            </div>
          ))}

          {/* Typing animation */}
          {loading && (
            <div className="msg bot typing">
              <span></span><span></span><span></span>
            </div>
          )}

          <div ref={bottomRef}></div>
        </div>

        {/* Input */}
        <div className="input-area">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about scriptures..."
          />
          <button onClick={handleAsk}>Send</button>
        </div>

      </div>
    </div>
  );
}

export default Chat;