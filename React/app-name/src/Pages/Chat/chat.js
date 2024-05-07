import React, { useState, useEffect } from 'react';
import ChatComponent from './ChatComponent';
import ChatList from "./ChatList";
import "./chat.css";

const ChatPage = () => {
  const [websocket, setWebsocket] = useState(null);
  const [userId, setUserId] = useState(null); // State to store the user ID
  const [messages, setMessages] = useState([]);

  const pass = async (username) => {
    const recipient_name = username;
    const response = await fetch(
      `http://localhost:8000/get_message/sender=${userId}&recipient=${recipient_name}`
    );
    const data = await response.json();
    setMessages(data);
  };

  useEffect(() => {
    // Function to retrieve the user ID from the token
    const getUserIdFromToken = () => {
      const token = document.cookie
        .split("; ")
        .find((row) => row.startsWith("token="))
        .split("=")[1];
      // Decode the token to get the user ID
      // Here you would use your actual decoding logic for JWT tokens
      const decodedToken = token;
      setUserId(decodedToken); // Set the user ID in the state
    };

    // Call the function to retrieve the user ID
    getUserIdFromToken();
  }, []); // Run only once when the component mounts

  useEffect(() => {
    if (userId) {
      const ws = new WebSocket(`ws://localhost:8000/ws/${userId}`);
      setWebsocket(ws);

      return () => {
        ws.close();
      };
    }
  }, [userId]); // Establish WebSocket connection when userId changes

  return (
    <div className="chat-page-container">
      <div className="left-side">
        <ChatList onUpdate={pass} />
      </div>
      <div className="right-side">
        {websocket && <ChatComponent log={messages} websocket={websocket} />}
      </div>
    </div>
  );
};

export default ChatPage;
