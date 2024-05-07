import React, { useState, useEffect } from 'react';

const ChatComponent = ({ userId, websocket, log, username, onEnter }) => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    setMessages([]);
    for (const key of log) {
      const { sender_username, content } = key;
      setMessages((prevMessages) => [
        ...prevMessages,
        `${sender_username}: ${content}`,
      ]);
    }
  }, [log]);

  const onServerCall = (data) => {
    if (data.trim() !== "") {
      websocket.send(JSON.stringify({ message: data, recipient: username }));
    }
    onEnter(username);
  };

  const onSubmit = (event) => {
    event.preventDefault();
    const data = document.querySelector("input.input-area").value;
    document.querySelector("input.input-area").value = "";
    onServerCall(data);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      const data = event.target.value;
      event.target.value = "";
      onServerCall(data);
    }
  };

  return (
    <div className="chat-component-container">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className="chat-message">
            <div className="content">{msg}</div>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          className="input-area"
          onKeyDown={handleKeyDown} // Add keydown event handler
          placeholder="Type a message..."
        />
        <button className="submit-button" onClick={onSubmit}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatComponent;
