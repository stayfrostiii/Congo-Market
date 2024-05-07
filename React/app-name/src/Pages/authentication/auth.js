import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Auth = () => {
  const navigate = useNavigate(); // Hook for navigation

  const handleSignUpClick = () => {
    navigate("/signup");
  };

  const handleLoginClick = () => {
    navigate("/login");
  };

  return (
    <div>
      <h2>Welcome to Our Marketplace!</h2>
      <p>Please select an option:</p>
      {/* Button to navigate to the sign-up page */}
      <button onClick={handleSignUpClick}>Sign Up</button>
      {/* Button to navigate to the login page */}
      <button onClick={handleLoginClick}>Log In</button>
      {/* Button to navigate back to the main page */}
      {/* <button onClick={handleGoToMainClick}>Go to Main Page</button> */}
    </div>
  );
};

export default Auth;
