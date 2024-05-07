import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainPage from "./pages/main-page/MainPage";
import AuthenticationSelectionPage from "./pages/authentication/AuthenticationSelectionPage";
import SignUpPage from "./pages/authentication/SignUpPage";
import LoginPage from "./pages/authentication/LoginPage";

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
      </Routes>
    </Router>
  );
}

export default App;
