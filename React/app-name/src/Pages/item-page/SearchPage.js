import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import "./SearchPage.css";
import lebron from "../../binary/lebron.jpg";
import { searchVIP } from "./ItemPage";

var itemPickedSP = 0;
let searchVSP = "";

const SearchPage = () => {
  useEffect(() => {
    handleSubmit();
  }, []);
  let [searchV, setSearchV] = useState("");
  const [message, setMessage] = useState("");
  const [tester, setTester] = useState("");
  const [counter, setCounter] = useState(0);
  const navigate = useNavigate(); // Hook for navigation

  const handleMainPageClick = () => 
  {
    navigate("/");
  };

  const handleItemClick = (id_get) =>
  {
    console.log("id = " + id_get + " searchV = " + searchVSP);
    itemPickedSP = id_get;
    navigate("/item_page");
  };

  const handleSubmit = async () => {
    try {
      if (searchVIP != "")
        searchV = searchVIP;
      console.log("Submitting item request:", { searchVIP });
      const response = await api.post("/query_item", { searchV: searchV });
      console.log("Response:", response.data);
      setMessage(response.data.message);
      setCounter(response.data.counter);
      setTester(response.data.tester);
      searchVSP = searchV;
      document.getElementById("search").value = searchV;
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
    console.log("info:" + tester);

    var indexComma = 0;
    var indexLine = 0;
    var indexSemi = 0;
    var indexPlus = 0;
    var itemCount = counter;
    let nameAdd = "";
    let price = "";
    var itemID = 0;

    let html = [];

    for (let i = 0; i < itemCount; i++) {
      indexSemi = items.indexOf(";");
      nameAdd = items.substring(0, indexSemi);

      indexComma = items.indexOf(",");
      const itemkey = items.substring(indexSemi + 1, indexComma);

      indexPlus = items.indexOf("^");
      price = items.substring(indexComma + 1, indexPlus);

      indexLine = items.indexOf("|");
      const itemID = items.substring(indexPlus + 1, indexLine);

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
              {nameAdd}, {itemID}
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
      <h1>Search</h1>
      {/* Button to navigate to the authentication selection page */}
      <button onClick={handleMainPageClick}>Go to MainPage</button>
      <br/>
      <input
        type="text"
        id="search"
        onChange={(e) => setSearchV(e.target.value)}
        placeholder="Enter Item"
      />

      <button onClick={handleSubmit}>Submit</button>
      <br />
      {/*<img src={lebron}/>*/}
      <div class="item-holder">{addDiv()}</div>
    </div>
  );
};

export { itemPickedSP, searchVSP };
export default SearchPage;
