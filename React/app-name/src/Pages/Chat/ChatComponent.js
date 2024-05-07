import React, { useState, useEffect } from 'react';

const ChatComponent = ({ userId, websocket, log, username, onEnter }) => {
  const [messages, setMessages] = useState([]);

  const caesarDecipher = (message, shift) => {
    return message.replace(/[a-zA-Z]/g, (char) => {
      const charCode = char.charCodeAt(0);
      const offset = charCode >= 65 && charCode <= 90 ? 65 : 97;
      // To handle negative shifts correctly, add 26 to ensure positive result
      return String.fromCharCode(
        ((charCode - offset - shift + 26) % 26) + offset
      );
    });
  };

  useEffect(() => {
    setMessages([]);
    for (const key of log) {
      const { sender_username, content } = key;
      const decryptedMessage = caesarDecipher(content, 3);
      setMessages((prevMessages) => [
        ...prevMessages,
        `${sender_username}: ${decryptedMessage}`,
      ]);
    }
  }, [log]);

  const caesarCipher = (message, shift) => {
    return message.replace(/[a-zA-Z]/g, (char) => {
      const charCode = char.charCodeAt(0);
      const offset = charCode >= 65 && charCode <= 90 ? 65 : 97;
      return String.fromCharCode(((charCode - offset + shift) % 26) + offset);
    });
  };

  const onServerCall = (data) => {
    if (data.trim() !== "") {
      const encryptedMessage = caesarCipher(data, 3);
      websocket.send(
        JSON.stringify({ message: encryptedMessage, recipient: username })
      );
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
