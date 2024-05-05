import React, { useState, useEffect } from 'react';
import ChatComponent from './ChatComponent';

const ChatPage = () => {
  const [websocket, setWebsocket] = useState(null);
  var clientId = Date.now()
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
 // Replace '123' with the client ID
    setWebsocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="chat-page-container">
      <div className="left-side">
        {/* Your chat list component goes here */}
      </div>
      <div className="right-side">
        {websocket && <ChatComponent websocket={websocket} />}
      </div>
    </div>
  );
};

export default ChatPage;
