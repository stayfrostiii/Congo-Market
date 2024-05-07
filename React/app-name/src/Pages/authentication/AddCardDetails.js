import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";

import Header from "../global/Header";

const CreditCardPage = () => {
  const [cardNumber, setCardNumber] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [cvv, setCvv] = useState("");
  const [message, setMessage] = useState("");
  const [userId, setUserId] = useState(null); // State to store the user ID
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    // Function to retrieve the user ID from the token
    const getUserIdFromToken = () => {
      const token = document.cookie
        .split("; ")
        .find((row) => row.startsWith("token="))
        .split("=")[1];

      // Extract the user ID from the token
      const userId = parseInt(token, 10);
      setUserId(userId); // Set the user ID in the state
    };

    // Call the function to retrieve the user ID
    getUserIdFromToken();
  }, []);

  const handleSubmit = async () => {
    try {
      console.log("Submitting credit card details:", {
        cardNumber,
        expiryDate,
        cvv,
      });
      const response = await api.post(`/add_card/${userId}`, {
        cardNumber,
        expiryDate,
        cvv,
      });
      console.log("Response:", response.data);
      setMessage(response.data.message);
      setCardNumber("");
      setExpiryDate("");
      setCvv("");
    } catch (error) {
      console.error("Error:", error);
      if (error.response) {
        console.error("Server responded with status:", error.response.status);
        console.error("Response data:", error.response.data);

        // Log validation errors
        console.log("Validation Errors:", error.response.data.detail);
      } else if (error.request) {
        console.error("No response received:", error.request);
      } else {
        console.error("Error setting up request:", error.message);
      }
      setMessage("An error occurred. Please try again later.");
    }
  };

  const handleGoBack = () => {
    navigate("/selection");
  };

  return (
    <div>
      <Header/>
      <h1>Enter Credit Card Details</h1>
      <label>Card Number:</label>
      <input
        type="text"
        value={cardNumber}
        onChange={(e) => setCardNumber(e.target.value)}
        placeholder="Enter your card number"
      />
      <label>Expiry Date:</label>
      <input
        type="text"
        value={expiryDate}
        onChange={(e) => setExpiryDate(e.target.value)}
        placeholder="MM/YY"
      />
      <label>CVV:</label>
      <input
        type="text"
        value={cvv}
        onChange={(e) => setCvv(e.target.value)}
        placeholder="Enter your CVV"
      />
      <button onClick={handleSubmit}>Submit Payment</button>
      <p>{message}</p>
      <button onClick={handleGoBack}>Go Back</button>
    </div>
  );
};

export default CreditCardPage;
