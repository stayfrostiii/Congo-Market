import React, { useEffect, useState } from 'react';
import axios from 'axios';

const FriendsList = () => {
  const [friends, setFriends] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/friends') // Adjust the URL based on your FastAPI server configuration
      .then(response => {
        setFriends(response.data);
      })
      .catch(error => {
        console.error('Error fetching friends:', error);
      });
  }, []);

  return (
    <div>
      <h1>Friends List</h1>
      <ul>
        {friends.map(friend => (
          <li key={friend.id}>
            {friend.first_name} {friend.last_name} ({friend.id_number})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FriendsList;