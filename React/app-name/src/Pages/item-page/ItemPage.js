import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import { itemPickedSP, searchVSP } from "./SearchPage";

let searchVIP = "";

const ItemProfile = () => 
{
  searchVIP = searchVSP;
  console.log("searchVSP = " + searchVSP);
  useEffect(() => {handleSubmit()}, []);
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // Hook for navigation

  const handleSubmit = async () => 
  {
    try 
    {
      const itemID = itemPickedSP;
      console.log("ID in info page: " + itemID);
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
    //console.log("here");
    navigate("/");
  };

  const handleSearchClick = () =>
  {
    navigate("/search_page");
  };

  const findNextPort = (port, portArr) =>
  {
    for (let i = 0; i < portArr.length; i++)
    {
      //console.log(portArr[i].substring(0,1));
      if (portArr[i].substring(0,1) == port)
      {
        console.log(portArr[i]);
        return portArr[i];
      }
    }
  }

  const reprice = () =>
  {
    // This variable will be the selected user's distribution center
    let buyerDC = "a";
    let sellerDC;
    var cost = 0;
    let temp;

    let aRoute = ["bb2", "cc1", "dc3", "ec4", "ff3", "gf4", "hc6"];
    let bRoute = ["aa2", "cc1", "dc3", "ec4", "fa5", "gc5", "hc6"];
    let cRoute = ["aa1", "bb1", "dd2", "ee3", "fe4", "ge4", "hd4"];
    let dRoute = ["ac3", "bc3", "cc3", "ee1", "fe2", "ge2", "hh2"];
    let eRoute = ["ac4", "bc4", "cc3", "dd1", "ff1", "gg1", "hh2"];
    let fRoute = ["aa3", "ba5", "ce4", "de2", "ee1", "gg1", "hh3"];
    let gRoute = ["af4", "be5", "ce4", "de2", "ee1", "ff1", "hh2"];
    let hRoute = ["ae6", "be6", "ce5", "dd2", "ee2", "fg3", "gg2"];

    switch(message[8])
    {
      case 1:
        sellerDC = "a";
        break;
      case 2:
        sellerDC = "b";
      break;
      case 3:
        sellerDC = "c";
      break;
      case 4:
        sellerDC = "d";
      break;
      case 5:
        sellerDC = "e";
      break;
      case 6:
        sellerDC = "f";
      break;
      case 7:
        sellerDC = "g";
      break;
      case 8:
        sellerDC = "h";
      break;
    }

    if (sellerDC != buyerDC)
      switch(sellerDC)
      {
        case "a":
          temp = findNextPort(buyerDC, aRoute);
          cost = parseInt(temp.substring(2,3));
          break;
        case "b":
          temp = findNextPort(buyerDC, bRoute);
          cost = parseInt(temp.substring(2,3));
          break;
        case "c":
          temp = findNextPort(buyerDC, cRoute);
          cost = parseInt(temp.substring(2,3));
          break;
        case "d":
          temp = findNextPort(buyerDC, dRoute);
          cost = parseInt(temp.substring(2,3));
          break;
        case "e":
          temp = findNextPort(buyerDC, eRoute);
          cost = parseInt(temp.substring(2,3));
          break;
        case "f":
          temp = findNextPort(buyerDC, fRoute);
          cost = parseInt(temp.substring(2,3));
          break;
        case "g":
          temp = findNextPort(buyerDC, gRoute);
          cost = parseInt(temp.substring(2,3));
          break;
        case "h":
          temp = findNextPort(buyerDC, hRoute);
          cost = parseInt(temp.substring(2,3));
          break;
      }
    return cost;
  }

  const addDiv = () => 
  {
    var addPrice = reprice();
    const html = message;
    //console.log(html);
    return (
    <div>
      <h1>{html[1]}</h1>
      <p>Item key: {html[0]}</p>
      <p>Price: ${html[4]} + ${addPrice}</p>
      <p>Description: {html[2]}</p>
      <p>Tags: {html[9]}</p>
      <p>Time: {html[5]}</p>
      <p>Date: {html[6]}</p>
      <p>Owner ID: {html[7]}</p>
      <p>Distribution Center: {html[8]}</p>
    </div>
    );
  }

  return (
        <div>
          <button onClick={handleMainpage}>Go to Main Page</button>
          <button onClick={handleSearchClick}>Search</button>
          <br/>
          <div>
              {addDiv()}
          </div>
        </div>
  );
};

export { searchVIP };
export default ItemProfile;