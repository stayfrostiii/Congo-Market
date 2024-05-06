import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainPage from "./Pages/main-page/MainPage";
import AuthenticationSelectionPage from "./Pages/authentication/AuthenticationSelectionPage";
import SignUpPage from "./Pages/authentication/SignUpPage";
import LoginPage from "./Pages/authentication/LoginPage";
import AddFriendForm from "./Pages/AddFriend/AddFriendForm";
import ChatPage from "./Pages/Chat/chat";
import ItemPage from "./Pages/item-page/ItemPage";
import AddItemPage from "./Pages/item-page/AddItemPage";
import SearchPage from "./Pages/item-page/SearchPage";

function App() {
  useEffect(() => {
    // Store the current page in localStorage whenever it changes
    localStorage.setItem("currentPage", window.location.pathname);
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/selection" element={<AuthenticationSelectionPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/add_friend" element={<AddFriendForm />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/item_page" element={<ItemPage />} />
        <Route path="/add_item" element={<AddItemPage />} />
        <Route path="/search_page" element={<SearchPage />} />
      </Routes>
    </Router>

    
  );
}

export default App;
