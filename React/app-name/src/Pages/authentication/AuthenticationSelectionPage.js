import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const AuthenticationSelectionPage = () => {
  const navigate = useNavigate(); // Hook for navigation

  const handleSignUpClick = () => {
    navigate("/signup");
  };

  const handleLoginClick = () => {
    navigate("/login");
  };

  const handleGoToMainClick = () => {
    navigate("/");
  };

  const handleFriendForm = () => {
    navigate("/add_friend")
  }
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
        userid: 123 // Replace with the actual user ID
      };

      // Make a request to save the file data to the congo database
      console.log("File data saved to the congo database");
    } catch (error) {
      console.error("Error uploading file:", error);
    }
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
      <button onClick={handleGoToMainClick}>Go to Main Page</button>

      <button onClick={handleFriendForm}>Friends</button>
      <button onClick={handleChatForm}>Chat</button>
      <form>
        <div>
          <button><input type="file" onChange={handleFileInputChange} /></button>
        </div>
        <button type="submit">Upload</button>
      </form>
      { file && <p>{file.name}</p>}
    </div>
  );
};

export default AuthenticationSelectionPage;
