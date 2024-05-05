import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import { itemPicked } from "../main-page/MainPage";

const ItemProfile = () => 
{
  useEffect(() => handleSubmit);
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // Hook for navigation
  const itemID = itemPicked;

  console.log("ID in info page: " + itemID);
  
  const handleSubmit = async () => 
  {
    try 
    {
      console.log("Submitting item request:", { itemID });
      const response = await api.post("/item_profile", { itemID: itemID });
      console.log("Response:", response.data);
      setMessage(response.data.message);
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

  const handleMainpage = () =>
  {
    console.log("here");
    navigate("/");
  }

  const addDiv = () => 
  {
    const html = {message};
    console.log(html);
    //const reactElement = parse(html);
    //console.log(reactElement);
    return (
    <div>
      <div dangerouslySetInnerHTML={{ __html: message }} />
    </div>
    );
  }

  return (
    <body>
        <div>
        <button onClick={handleMainpage}>Go to Main Page</button>
        <br/>
        <div class="item-holder">
            {addDiv()}
        </div>
        </div>
    </body>
  );
};

export default ItemProfile;