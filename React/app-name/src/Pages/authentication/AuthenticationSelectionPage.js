import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import DeleteAccountButton from "./DeleteAccountButton";
import "./MainPage.css";

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

  navigate("/chat")
  }
  const [file, setFile] = useState(null);


  const handleFileInputChange = async (event) => {
    console.log(event)
    const file = event.target.files[0];
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/files", formData);
      console.log("File uploaded successfully:", response.data);

      // Save the file to the locally stored congo database in the file category
      const fileData = {
        name: file.name,
        contents: file, // Pass the file object directly
        userid: 123, // Replace with the actual user ID
      };

      // Make a request to save the file data to the congo database
      console.log("File data saved to the congo database");
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div>
    <Header/>
    <br/>
      <h1 class="title">Welcome to Our Marketplace!</h1>
      {/* Button to navigate back to the main page */}
      <div class="content">
        <div>
          <button onClick={handleAuthentication}>Sign Out</button>
          <DeleteAccountButton /> {/* Render the DeleteAccountButton component */}
        </div>
        <br/>
        <form>
          <button><input type="file" onChange={handleFileInputChange} /></button>
          <button type="submit">Upload</button>
        </form>
        { file && <p>{file.name}</p>}
      </div>
    </div>
  );
};

export default AuthenticationSelectionPage;
