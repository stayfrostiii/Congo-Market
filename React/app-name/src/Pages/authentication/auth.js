import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import logo from "../../binary/logo.jpg";
import "./auth.css";

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
      <div class="content">
        <img id="header-img" src={logo}/>
        <br/>
        <h2>Welcome to Our Marketplace!</h2>
        <p>Please select an option:</p>
        {/* Button to navigate to the sign-up page */}
        <div>
          <button onClick={handleSignUpClick}>Sign Up</button>
          {/* Button to navigate to the login page */}
          <button onClick={handleLoginClick}>Log In</button>
          {/* Button to navigate back to the main page */}
          {/* <button onClick={handleGoToMainClick}>Go to Main Page</button> */}
        </div>
      </div>
    </div>
  );
};

export default Auth;
