import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import "./LoginSignUp.css";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // Hook for navigation

  const handleSubmit = async () => {
    try {
      console.log("Submitting login request:", { email, password });
      const response = await api.post("/login", {
        email: encrypt(email),
        password: encrypt(password),
      });

      console.log("Response:", response.data);

      // Assuming the response contains a token field
      const token = response.data.token;

      // Set the token as an HTTP-only cookie
      document.cookie = `token=${token}; Path=/; SameSite=Strict`;

      // Redirect the user to another page, e.g., dashboard
      navigate("/selection");
    } catch (error) {
      console.error("Error:", error);
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error("Server responded with status:", error.response.status);
        console.error("Response data:", error.response.data);
      } else if (error.request) {
        // The request was made but no response was received
        console.error("No response received:", error.request);
      } else {
        // Something happened in setting up the request that triggered an error
        console.error("Error setting up request:", error.message);
      }
      // Display a generic error message to the user
      setMessage("An error occurred. Please try again later.");
    }
  };

  const encrypt = (data) => {
    // Perform encryption logic here
    return data;
  };

  const handleGoBack = () => {
    navigate("/selection");
  };

  return (
    <div class="agesdgvadfbb">
      <br/>
      <h1>Login Page</h1>
      <div>
        <label>Email:</label>
        <input
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
        />
      </div>
      <br/>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
        />
      </div>
      <br/>
      <div>
        <button onClick={handleSubmit}>Login</button>
        <p>{message}</p>
        {/* Button to navigate back to the authentication selection page */}
      </div>
    </div>
  );
};

export default LoginPage;
