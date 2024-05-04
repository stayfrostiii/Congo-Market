import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";

const MainPage = () => 
{
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [counter, setCounter] = useState("");
  const navigate = useNavigate(); // Hook for navigation
  var itemCount = 0;

  const handleAuthenticationClick = () => 
  {
    navigate("/selection");
  };

  const handleSubmit = async () => 
  {
    try 
    {
      console.log("Submitting item request:", { name });
      const response = await api.post("/query_item", { name: name, });
      console.log("Response:", response.data);
      setMessage(response.data.message);
      setCounter(response.data.counter);
      setName("");
    } 
    catch (error) 
    {
      console.error("Error:", error);
      if (error.response) 
      {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error("Server responded with status:", error.response.status);
        console.error("Response data:", error.response.data);
      } 
      else if (error.request) 
      {
        // The request was made but no response was received
        console.error("No response received:", error.request);
      } 
      else 
      {
        // Something happened in setting up the request that triggered an error
        console.error("Error setting up request:", error.message);
      }
      // Display a generic error message to the user
      setMessage("An error occurred. Please try again later.");
    }
  };

  const addDiv = () => 
  {
    itemCount = {counter};
    itemCount = 1;
    while (itemCount--)
    {
      return (  
        <div>
          <p> {message[itemCount]} </p>
        </div>);
    }
  }

  return (
    <div>
      <h1>Welcome to Our Marketplace!</h1>
      <p>This is the main page content.</p>
      {/* Button to navigate to the authentication selection page */}
      <button onClick={handleAuthenticationClick}>Go to Authentication</button>
      <br/>
      <input type="text" onChange={(e) => setName(e.target.value)} placeholder="Enter name"/>
      <button onClick={handleSubmit}>Login</button>
      {addDiv()}
    </div>
  );
};

export default MainPage;
