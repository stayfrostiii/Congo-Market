import React, { useState } from 'react';
import axios from 'axios';
import FriendsList from "../../FriendsList";
import './AddFriendForm.css'

const AddFriendForm = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [idNumber, setIdNumber] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Send a POST request to the backend to add the friend
    axios.post('http://localhost:8000/friends', {
      first_name: firstName,
      last_name: lastName,
      id_number: idNumber
    })
    .then(response => {
      console.log('Friend added successfully:', response.data);
      // Clear the form after successfully adding the friend
      setFirstName('');
      setLastName('');
      setIdNumber('');
    })
    .catch(error => {
      console.error('Error adding friend:', error);
    });
  };

  return (
    <div className='friend-container'>
        <div className='form-container'>
            <h2 className='friend-header'>Add Friend</h2>
            <form onSubmit={handleSubmit}>
                <label>
                First Name:
                <input className='fname' type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                </label>
                <br />
                <br />
                <label>
                Last Name:
                <input className='lname' type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                </label>
                <br />
                <br />
                <label>
                ID Number:
                <input className='idnum' type="text" value={idNumber} onChange={(e) => setIdNumber(e.target.value)} />
                </label>
                <br />
                <br />
                <button className='submit-button' type="submit">Add Friend</button>
            </form>
        </div> 

        <div className='friendList'>
            <div>
                <FriendsList /> {/* Use the FriendsList component */}
            </div>
        </div>

    </div>
    
  );
};

export default AddFriendForm;
