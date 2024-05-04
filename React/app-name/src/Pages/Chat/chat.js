import React from 'react';
import ChatList from './ChatList.js'; // Assuming you have a ChatList component
import ChatComponent from './ChatComponent'; 
import './chat.css'; 

const ChatPage = () => {
  return (
    <div className="chat-page-container">
      <div className="left-side">
        <ChatList />
      </div>
      <div className="right-side">
        <ChatComponent />
      </div>
    </div>
  );
};

export default ChatPage;
