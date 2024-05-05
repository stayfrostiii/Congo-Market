import React, { useState, useEffect } from 'react';

const ChatComponent = ({ websocket }) => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Event listener for incoming messages
    websocket.onmessage = (event) => {
      const data = event.data; 
      setMessages((prevMessages) => [...prevMessages, data]);
    };

    return () => {
      // Cleanup function
      websocket.onmessage = null;
    };
  }, [websocket]);

  const handleSendMessage = () => {
    if (message.trim() !== '') {
      websocket.send(JSON.stringify({ message }));
      setMessage('');
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSendMessage();
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
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown} // Add keydown event handler
          placeholder="Type a message..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatComponent;
