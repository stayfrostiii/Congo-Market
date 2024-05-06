import React, { useState, useEffect } from "react";

const ChatList = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [userSuggestions, setUserSuggestions] = useState([]);

  // Function to fetch user suggestions from the backend
  const fetchUserSuggestions = async (query) => {
    try {
      // Make a request to the backend API to fetch user suggestions based on the query
      const response = await fetch(`/api/users?q=${query}`);
      const data = await response.json();
      setUserSuggestions(data.users);
    } catch (error) {
      console.error("Error fetching user suggestions:", error);
    }
  };

  // Event handler for typing in the search bar
  const handleSearchInputChange = (event) => {
    const query = event.target.value;
    setSearchQuery(query);
    fetchUserSuggestions(query); // Fetch user suggestions as the user types
  };

  return (
    <div className="chat-list-container">
      <input
        type="text"
        value={searchQuery}
        onChange={handleSearchInputChange}
        placeholder="Search for users..."
        className="search-input"
      />
      {userSuggestions.length > 0 && (
        <ul className="user-suggestions">
          {userSuggestions.map((user) => (
            <li key={user.id}>{user.username}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ChatList;
