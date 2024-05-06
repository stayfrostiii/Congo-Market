import React from "react";
import { useNavigate } from "react-router-dom";

const MainPage = () => {
  const navigate = useNavigate(); // Hook for navigation

  const handleAuthenticationClick = () => {
    navigate("/selection");
  };

  return (
    <div>
      <h1>Welcome to Our Marketplace!</h1>
      <p>This is the main page content.</p>
      {/* Button to navigate to the authentication selection page */}
      <button onClick={handleAuthenticationClick}>Go to Authentication</button>
    </div>
  );
};

export default MainPage;
