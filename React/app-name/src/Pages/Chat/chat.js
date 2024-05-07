import React, { useState, useEffect } from 'react';
import ChatComponent from './ChatComponent';
import ChatList from "./ChatList";
import "./chat.css";

import Header from "../global/Header";

const ChatPage = () => {
  const [websocket, setWebsocket] = useState(null);
  const [userId, setUserId] = useState(null); // State to store the user ID

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

    const ws = new WebSocket(`ws://localhost:8000/ws/${userId}`);
    setWebsocket(ws);

    return () => {
      ws.close();
    };
  }, [userId]);

  return (
    <div class="overall">
      <Header/>
      <div className="chat-page-container">
        <div className="left-side">
          <ChatList />
        </div>
        <div className="right-side">
          {websocket && <ChatComponent websocket={websocket} />}
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
