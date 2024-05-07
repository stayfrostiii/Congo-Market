import React, { useState, useEffect } from "react";
import ChatComponent from "./ChatComponent";

const ChatList = ({ onUpdate }) => {
  const [usernames, setUsernames] = useState([]);
  const [client_id, setclientId] = useState(null); // State to store the user ID
  const [messages, setMessages] = useState([]); // State to store messages

  useEffect(() => {
    fetchUsernames();
  }, []);

  useEffect(() => {
    // Function to retrieve the user ID from the token
    const getUserIdFromToken = () => {
      const token = document.cookie
        .split("; ")
        .find((row) => row.startsWith("token="))
        .split("=")[1];
      // Decode the token to get the user ID
      // Here you would use your actual decoding logic for JWT tokens
      const decodedToken = token;
      setclientId(decodedToken); // Set the user ID in the state
    };

    // Call the function to retrieve the user ID
    getUserIdFromToken();
  }, []); // Run only once when the component mounts

  const fetchUsernames = async () => {
    try {
      const response = await fetch("http://localhost:8000/search_users");
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const text = await response.text(); // Get the response text
      const data = JSON.parse(text); // Parse the response text as JSON
      setUsernames(data);
      console.log("Parsed data:", data);
    } catch (error) {
      console.error("Error parsing JSON:", error);
    }
  };

  const handleSearchInputChange = async (event) => {};

  const onEnter = async (event) => {
    if (event.key === "Enter") {
      onUpdate(event.currentTarget.value);
      // const recipient_name = event.currentTarget.value;
      // const response = await fetch(
      //   `http://localhost:8000/get_message/sender=${client_id}&recipient=${recipient_name}`
      // );
      // const messages = await response.json();
      // console.log(messages);
    }
  };

  return (
    <div>
      <div className="chat-list-container">
        <input
          type="text"
          onChange={handleSearchInputChange}
          onKeyDown={onEnter}
          placeholder="Search for users..."
          className="search-input"
        />
      </div>

      <div className="usernames-container">
        <h2>All Usernames</h2>
        <ul className="user-list">
          {usernames.map((username, index) => (
            <li key={index}>{username}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
export default ChatList;

