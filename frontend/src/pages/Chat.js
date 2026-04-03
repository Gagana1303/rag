import { useState, useRef, useEffect } from "react";
import { askQuestion } from "../services/api";

function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef();

  // 🔥 Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const updated = [...messages, { type: "user", text: question }];
    setMessages(updated);
    setQuestion("");
    setLoading(true);

    try {
      const res = await askQuestion({
        question,
        scripture: "mahabharata", // fixed for now
      });

      setMessages([
        ...updated,
        { type: "bot", text: res.data.answer },
      ]);
    } catch {
      setMessages([
        ...updated,
        { type: "bot", text: "Error fetching answer" },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="divine-bg">
      <div className="chat-container">

        {/* CHAT BOX */}
        <div className="chat-box">
          {messages.length === 0 && (
            <div className="chat-message bot">
              Ask anything about scriptures 
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`chat-message ${msg.type}`}>
              {msg.text}
            </div>
          ))}

          {/* Typing animation */}
          {loading && (
            <div className="chat-message bot">
              Typing...
            </div>
          )}

          <div ref={bottomRef}></div>
        </div>

        {/* INPUT */}
        <div className="chat-input">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about scriptures..."
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          />
          <button onClick={handleAsk}>Ask</button>
        </div>

      </div>
    </div>
  );
}

export default Chat;
