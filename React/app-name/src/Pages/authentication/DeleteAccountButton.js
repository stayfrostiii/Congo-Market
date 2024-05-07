import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";

const DeleteAccountButton = () => {
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

  const handleDeleteAccount = async () => {
    try {
      if (!userId) {
        console.error("User ID not available");
        return;
      }

      // Send a DELETE request to delete the account
      console.log("Deleting account for user ID:", userId);
      const response = await api.post(`/delAccount/${userId}`);

      // Handle the response from the server
      navigate("/");
      document.cookie = `token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT`;
      if (response.ok) {
        console.log("Account deleted successfully");
        // Perform any necessary actions after successful deletion (e.g., redirect, show a message)
      } else {
        console.error("Failed to delete account");
        // Handle error response from the server
      }
    } catch (error) {
      console.error("Error:", error);
      // Handle other types of errors (e.g., network error)
    }
  };

  return <button onClick={handleDeleteAccount}>Delete Account</button>;
};

export default DeleteAccountButton;
