import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import Header from "../global/Header";

const AuthenticationSelectionPage = () => {
  const navigate = useNavigate(); // Hook for navigation

  const handleAuthentication = () => {
    document.cookie = `token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT`;
    navigate("/");
  };

  const handleCreditForm = () => {
    navigate("/card");
  };

  const handleGoToMainClick = () => {
    navigate("/main_page");
  };

  const handleFriendForm = () => {
    navigate("/add_friend");
  };
  const handleChatForm = () => {
    navigate("/chat");
  };

  const handleFileInputChange = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("/api/upload", formData);
      console.log("File uploaded successfully:", response.data);

      // Save the file to the locally stored congo database in the file category
      const fileData = {
        name: file.name,
        contents: file, // Pass the file object directly
        userid: 123, // Replace with the actual user ID
      };

      // Make a request to save the file data to the congo database
      await axios.post("sqlite:///./congo.db", fileData); // Replace "/api/files" with the appropriate API endpoint
      console.log("File data saved to the congo database");
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };
  const handleSubmit = async () => {
    try {
      // Get the uploaded file data from the locally stored congo database
      const response = await axios.get("sqlite:///./congo.db");
      const fileData = response.data;

      // Submit the file data to the table
      await axios.post("sqlite:///./congo.db", fileData); // Replace "/api/submit" with the appropriate API endpoint
      console.log("File data submitted to the table");
    } catch (error) {
      console.error("Error submitting file data:", error);
    }
  };



  return (
    <div>
    <Header/>
      <h2>Welcome to Our Marketplace!</h2>
      <p>Please select an option:</p>
      {/* Button to navigate back to the main page */}
      <button onClick={handleAuthentication}>Accounts</button>
      <button onClick={handleCreditForm}>Credit Card</button>
      <button onClick={handleGoToMainClick}>Go to Main Page</button>

      <button onClick={handleFriendForm}>Friends</button>
      <button onClick={handleChatForm}>Chat</button>
      <button>
        <input type="file" onChange={handleFileInputChange} />
      </button>

      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default AuthenticationSelectionPage;
