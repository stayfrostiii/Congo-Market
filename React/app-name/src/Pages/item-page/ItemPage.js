import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import { itemPickedSP, searchVSP } from "./SearchPage";
import { itemPickedMP } from "./YourItems";

import Header from "../global/Header";

let searchVIP = "";

const ItemProfile = () => 
{
  const [userId, setUserId] = useState(null); // State to store the user ID
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // Hook for navigation

  searchVIP = searchVSP;
  console.log("searchVSP = " + searchVSP);
  useEffect(() => {
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
  }, []);

  useEffect(() => {
    handleSubmit();
  }, []);

  const handleSubmit = async () => 
  {
    try 
    {
      let itemkey;
      if (itemPickedMP == "")
      {
        itemkey = itemPickedSP;
      }
      else 
      {
        itemkey = itemPickedMP;
      }
      console.log("ID in info page: " + itemkey);
      console.log("Submitting item request:", { itemkey });
      const response = await api.post("/item_profile", { itemkey: itemkey });
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

    if (message[8] != buyerDC)
      switch(message[8])
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
          <Header/>
          <br/>
          <div class="title">
            <h1 class="title">Item Info</h1>
            <br/>
            <div>
                {addDiv()}
            </div>
          </div>
        </div>
  );
};

export { searchVIP };
export default ItemProfile;