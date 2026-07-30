import { useEffect, useRef, useState } from "react";
import { Send, Bot, User, Loader2 } from "lucide-react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "assistant",
      content:
        "Hi Rahul! 👋 Welcome to Acme Corp's Time-Off Assistant. How can I help you today?",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);
  const handleSend = async () => {
    const text = input.trim();

    if (!text || loading) {
      return;
    }

    // Add user message immediately
    const userMessage = {
      id: Date.now(),
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Temporary fake response until FastAPI is connected
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: text,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: data.response,
      };

      setMessages((prev) => [...prev, assistantMessage]);

    } catch (error) {

      console.error("Chat API error:", error);

      const errorMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content:
          "Sorry, I couldn't connect to the Acme backend. Please make sure the API server is running.",
      };

      setMessages((prev) => [...prev, errorMessage]);

    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        {/* Header */}
        <header className="chat-header">
          <div className="header-icon">
            <Bot size={24} />
          </div>

          <div>
            <h1>Acme Time-Off Assistant</h1>
            <div className="status">
              <span className="status-dot"></span>
              Online
            </div>
          </div>
        </header>

        {/* Messages */}
        <main className="messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message-row ${message.role === "user" ? "user-row" : "assistant-row"
                }`}
            >
              {message.role === "assistant" && (
                <div className="avatar assistant-avatar">
                  <Bot size={18} />
                </div>
              )}

              <div
                className={`message ${message.role === "user"
                  ? "user-message"
                  : "assistant-message"
                  }`}
              >
                {message.content}
              </div>

              {message.role === "user" && (
                <div className="avatar user-avatar">
                  <User size={18} />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message-row assistant-row">
              <div className="avatar assistant-avatar">
                <Bot size={18} />
              </div>

              <div className="message assistant-message typing">
                <Loader2 size={18} className="spin" />
                Thinking...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </main>

        {/* Input */}
        <footer className="input-area">
          <div className="input-wrapper">
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about your leave, balance, or policy..."
              rows={1}
              disabled={loading}
            />

            <button
              className="send-button"
              onClick={handleSend}
              disabled={!input.trim() || loading}
              title="Send message"
            >
              <Send size={19} />
            </button>
          </div>

          <p className="input-hint">
            Press Enter to send · Shift + Enter for a new line
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;