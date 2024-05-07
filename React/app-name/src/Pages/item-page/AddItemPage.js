import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import "./AddItem.css";

const AddItemPage = () => 
{
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [price, setPrice] = useState(0);
  const [uTags, setTags] = useState("");
  const [message, setMessage] = useState("");
  const [pTag, setPTag] = useState("");
  const navigate = useNavigate(); // Hook for navigation
  let tags;
  
  const handleMainPageClick = () => 
  {
    navigate("/main_page");
  };

  const handleSubmit = async () => 
  {
    try 
    {
      if (pTag == "") throw "deez nuts";
      tags = pTag + ";" + uTags;
      console.log("Submitting item request:", { name, desc, price, tags });
      const response = await api.post("/add_item", { 
        name: name,
        desc: desc,
        price: price,
        tags
      });
      console.log("Response:", response.data);
      setMessage(response.data.message);
      setName("");
      setDesc("");
      setPrice("");
      setTags("");
      setPTag("");
      document.getElementById("name").value = "";
      document.getElementById("desc").value = "";
      document.getElementById("price").value = "";
      document.getElementById("tag").value = "";
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

  return (
    <div>
      <h1>Add Item</h1>
      <button onClick={handleMainPageClick}>Go to Main Page</button>
      <br/>
      <br/>
      <input type="text" id="name" onChange={(e) => setName(e.target.value)} placeholder="Enter Name"/>
      <br/>
      <input type="text" id="desc"  onChange={(e) => setDesc(e.target.value)}  placeholder="Enter Description"/>
      <br/>
      <input type="text" id="price"  onChange={(e) => setPrice(e.target.value)}  placeholder="Enter Price"/>
      <br/>
      <label for="tags">Select Preset Tag:&nbsp;</label>
        <select name="tags" onChange={(e) => setPTag(e.target.value)}>
            <option value="" disabled selected hidden></option>
            <option value="A">Book/Movie</option>
            <option value="B">Electronics</option>
            <option value="C">Computers</option>
            <option value="D">Garden/Tools</option>
            <option value="E">Beauty/Health</option>
            <option value="F">Toys</option>
            <option value="G">Handmade</option>
            <option value="H">Sports/Outdoors</option>
            <option value="I">Automotive/Industrial</option>
            <option value="J">Collectibles</option>
            <option value="K">Other</option>
        </select>
      <br/>
      <input type="text" id="tag"  onChange={(e) => setTags(e.target.value)}  placeholder="Enter Tags (separate by ;)"/>
      <br/>
      <br/>
      <button onClick={handleSubmit}>Submit</button>
      <br/>
      {message}
    </div>
  );
};

export default AddItemPage;