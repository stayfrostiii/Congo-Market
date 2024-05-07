import React, { useState, useEffect } from 'react';

const ChatComponent = ({ websocket, log }) => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    setMessages([]);

    for (const key in log) {
      if (Array.isArray(log[key])) {
        for (const item of log[key]) {
          setMessages((prevMessages) => [...prevMessages, `${key}: ${item}`]);
        }
      }
    }

    // log = {"1" : ["asdf", "asdf", "Gay"]}
    // for (const key in log) => key === "1"
    // log.get("1") === isArray?
    // for (const item of log[key]) => item = every item in the array
  }, [log]);

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      const data = event.target.value;
      event.target.value = "";
      setMessages((prevMessages) => [...prevMessages, data]);
      if (data.trim() !== "") {
        websocket.send(JSON.stringify({ message: data }));
      }
    }
  };

  return (
    <div className="chat-component-container">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message`}>
            <div className="content">{msg}</div>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          onKeyDown={handleKeyDown} // Add keydown event handler
          placeholder="Type a message..."
        />
      </div>
    </div>
  );
};

export default ChatComponent;

//<button onClick={handleSendMessage}>Send</button>