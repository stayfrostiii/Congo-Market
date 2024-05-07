import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import "./MainPage.css";
import lebron from "../../binary/lebron.jpg";

let itemPicked = 0;

const MainPage = () => {

  const [userId, setUserId] = useState(null); // State to store the user ID
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [counter, setCounter] = useState(0);
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    handleSubmit();
    // Function to retrieve the user ID from the token
    const getUserIdFromToken = () => {
      console.log("id:" + document.cookie);
      const token = document.cookie
        .split("; ")
        .find((row) => row.startsWith("token="))
        .split("=")[1];
      // Decode the token to get the user ID
      // Here you would use your actual decoding logic for JWT tokens
      const decodedToken = token;
      setUserId(decodedToken); // Set the user ID in the state
    };

    // Call the function to retrieve the user ID
    getUserIdFromToken();

  }, [userId], []);

  const handleAuthenticationClick = () => {
    navigate("/selection");
  };

  const handleSearchClick = () =>
  {
    navigate("/search_page");
  };

  const handleAddItemClick = () =>
  {
    navigate("/add_item");
  };


  const handleItemClick = (id_get) =>
  {
    //console.log(id_get);
    itemPicked = id_get;
    navigate("/item_page");
  };

  const handleSubmit = async () => {
    try {
      console.log("Submitting item request:", { name });
      const response = await api.post("/query_item", { name: name });
      console.log("Response:", response.data);
      setMessage(response.data.message);
      setCounter(response.data.counter);
      setName("");
      document.getElementById("search").value = "";
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

  const addDiv = () => {
    let items = message;
    //console.log("Add div:" + message);

    var indexComma = 0;
    var indexLine = 0;
    var indexSemi = 0;
    var itemCount = counter;
    let name = "";
    let price = "";
    var itemID = 0;

    let html = [];

    for (let i = 0; i < itemCount; i++) {
      indexComma = items.indexOf(",");
      name = items.substring(0, indexComma);

      indexSemi = items.indexOf(";");
      price = items.substring(indexComma + 1, indexSemi);

      indexLine = items.indexOf("|");
      const itemID = parseInt(items.substring(indexSemi + 1, indexLine));

      items = items.substring(indexLine + 1);

      //console.log("id: " + itemID);

      html.push(
        <div>
          <button class="item" onClick={() => handleItemClick(itemID)}>
            <div class="indicators">
              <p class="trade-ind"></p>
              <p class="friend-ind"></p>
            </div>
            <img class="image" src={lebron} alt="" />
            <p class="item-name">
              {name}, {itemID}
            </p>
            <p class="price">${price}</p>
          </button>
        </div>
      );

      //console.log(i + " - " + name + " " + price + " " + itemID);
    }

    return html;
  };

  return (
    <div>
      <h1>Welcome to Our Marketplace!</h1>
      <p>This is the main page content.</p>
      {/* Button to navigate to the authentication selection page */}
      <button onClick={handleAuthenticationClick}>Go to Authentication</button>
      <button onClick={handleSearchClick}>Search</button>
      <button onClick={handleAddItemClick}>Add Item</button>
      <p>{userId}</p>
      <input
        type="hidden"
        id="search"
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter Item"
      />
      <br/>
      {/*<img src={lebron}/>*/}
      <div class="item-holder">{addDiv()}</div>
    </div>
  );
};

export { itemPicked };
export default MainPage;
