import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./AddFriendForm.css";

const AddFriendForm = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [idNumber, setIdNumber] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // Hook for navigation

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send a POST request to the backend to add the friend
      const response = await axios.post("http://localhost:8000/friends", {
        firstName: firstName,
        lastName: lastName,
        idNumber: idNumber,
      });
      console.log("Friend added successfully:", response.data);
      // Clear the form after successfully adding the friend
      setFirstName("");
      setLastName("");
      setIdNumber("");
      setMessage("Friend added successfully");
    } catch (error) {
      console.error("Error adding friend:", error);
      setMessage("An error occurred. Please try again later.");
    }
  };

  const handleGoBack = () => {
    navigate("/selection");
  };

  return (
    <div>
      <h2 className="friend-header">Add Friend</h2>
      <form onSubmit={handleSubmit}>
        <label>
          First Name:
          <input
            className="fname"
            type="text"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />
        </label>
        <br />
        <br />
        <label>
          Last Name:
          <input
            className="lname"
            type="text"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
        </label>
        <br />
        <br />
        <label>
          ID Number:
          <input
            className="idnum"
            type="text"
            value={idNumber}
            onChange={(e) => setIdNumber(e.target.value)}
          />
        </label>
        <br />
        <br />
        <button className="submit-button" type="submit">
          Add Friend
        </button>
      </form>
      <p>{message}</p>
      {/* Button to navigate back to the authentication selection page */}
      <button onClick={handleGoBack}>
        Go Back to Authentication Selection
      </button>
    </div>
  );
};

export default AddFriendForm;