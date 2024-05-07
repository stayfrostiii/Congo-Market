import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./AddFriendForm.css";

import Header from "../global/Header";

// Node class for linked list
class Node {
  constructor(firstName, lastName, idNumber) {
    this.firstName = firstName;   //this = current instance of class, similar to C++
    this.lastName = lastName;
    this.idNumber = idNumber;
    this.next = null;
  }
}

// Linked list class
class LinkedList {
  constructor() {
    this.head = null;
  }

  append(firstName, lastName, idNumber) {
    const newNode = new Node(firstName, lastName, idNumber);
    if (!this.head) {
      this.head = newNode;
    } else {
      let current = this.head;
      while (current.next) {
        current = current.next;
      }
      current.next = newNode;
    }
  }

  toArray() {       //Turns the linked list into an array
    const result = [];
    let current = this.head; 
    while (current) {
      result.push(current);   //add node to end of result array
      current = current.next;
    }
    return result;
  }

  quicksort() {
    // Implement quicksort algorithm
    // This is a simplified version for demonstration purposes
    // You may need to modify it for better performance and edge cases handling
    const sort = (list) => {        //sort arrow function that takes in parameter list 
      if (!list || !list.length) {
        return [];
      }
      const pivot = list[0];      //pivot is first element of list
      const smaller = [];
      const greater = [];
      for (let i = 1; i < list.length; i++) {
        if (list[i].firstName < pivot.firstName) {
          smaller.push(list[i]);                  //if firstname of elements in list are lower letters, they get added to end of "smaller" array
        } else {
          greater.push(list[i]);                  //if firstname of elements in list are higher letters, they get added to end of "higher" array
        }
      }
      return sort(smaller).concat(pivot, sort(greater));      //recursively sort the smaller and greater arrays until they are properly sorted, then concatenate them together to form one single sorted array
    };
    const sorted = sort(this.toArray());    //first turns linked list into an array, then passing that linked list transformed array into the sort function that was just created
    this.head = sorted[0];                  //because sorted now, put the first "least value" element/first name into the head of the linked list
    let current = this.head;                //linked list traversal
    for (let i = 1; i < sorted.length; i++) {
      current.next = sorted[i];             //since sorted is now a sorted array, we can add it to each linked list index
      current = current.next;           //iterate/traverse
    }
    current.next = null;          
  }

  binarySearch(firstName) {
    let left = 0;
    let right = this.toArray().length - 1;  // Convert linked list to array for binary search

    while (left <= right) {
      let mid = Math.floor((left + right) / 2);
      if (this.toArray()[mid].firstName === firstName) {
        return true;  // Friend found
      } else if (this.toArray()[mid].firstName < firstName) {   //if middle element is less than arg, then make left traversal start from middle and go higher
        left = mid + 1;
      } else {    //implies middle element is greated, so keep going down from right side
        right = mid - 1;
      }
    }

    return false;  // Friend does not exist
  }

}

const AddFriendForm = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [idNumber, setIdNumber] = useState("");
  const [deleteID, setDeleteID] = useState("");
  const [message, setMessage] = useState("");
  const [friends, setFriends] = useState([]);

  const [searchFirstName, setSearchFirstName] = useState("");


  const navigate = useNavigate(); // Hook for navigation


  const handleGoBack = () => {
    navigate("/selection");
  };


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

  
  const handleDelete = async (e) => {
    e.preventDefault();
    try {
      // Send a DELETE request to the backend to delete the friend
      const response = await axios.delete(`http://localhost:8000/friends/${deleteID}`);
      console.log("Friend deleted successfully:", response.data);
      // Clear the form after successfully deleting the friend
      setDeleteID("");
      setMessage("Friend deleted successfully");
    } catch (error) {
      console.error("Error deleting friend:", error);
      setMessage("An error occurred. Please try again later.");
    }
  };

  const fetchFriendsList = async () => {
    try {
      // Send a GET request to the backend to fetch the friends list
      const response = await axios.get("http://localhost:8000/friends");
      if (response.data.length === 0) {
        // If the response data is empty, set friends to an empty array
        setFriends([]);   //set friends to an empty state if there is no data in friends_list column (Because it is all deleted)
      } else {
        // Convert the fetched data into a linked list
        const linkedList = new LinkedList();
        response.data.forEach((friend) => {
          linkedList.append(friend.firstName, friend.lastName, friend.idNumber);  //add each piece of data retrieved from sql database into the linked list
        });

        linkedList.quicksort();           //quicksorts the linkedlist by first name

        setFriends(linkedList.toArray());   //turns linked list into an array to be able to change state of friends
      }
    } catch (error) {
      console.error("Error fetching friends list:", error);
    }
};

  useEffect(() => {
      // Fetch friends list when component mounts
      fetchFriendsList();
  }, [idNumber, deleteID]);     //runs every time idNumber or deleteID is modified

  const handleSearch = async () => {

   try {
     // Send a GET request to the backend to fetch the friends list
     const response = await axios.get("http://localhost:8000/friends");
     if (response.data.length === 0) {
       // If the response data is empty, set friends to an empty array
       setFriends([]);   //set friends to an empty state if there is no data in friends_list column (Because it is all deleted)
     } else {
       // Convert the fetched data into a linked list
       const linkedList = new LinkedList();
       response.data.forEach((friend) => {
         linkedList.append(friend.firstName, friend.lastName, friend.idNumber);  //add each piece of data retrieved from sql database into the linked list
       });
       linkedList.quicksort(); //possibly delete if it doesn't make program faster
       const isFound = linkedList.binarySearch(searchFirstName);
        if (isFound) {
          setMessage(`Friend ${searchFirstName} found.`);
        } else {
          setMessage(`Friend ${searchFirstName} does not exist.`);
     }
      }
    }
    catch (error) {
      console.error("Error fetching friends list:", error);
    }
   };

  return (
    <div>
      <Header/>
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

      <form onSubmit={handleDelete}>
        <label>
          ID Number:
          <input
            className="idnum"
            type="text"
            value={deleteID}
            onChange={(e) => setDeleteID(e.target.value)}
          />
        </label>
        <br />
        <br />
        <button className="submit-button" type="submit">
          Delete Friend
        </button>
      </form>

        {/* Display the friends list */}
      <div>
        <h2 className="friends-header">Friends List</h2>
        <table>
          <thead>
            <tr>
              <th>First Name</th>
              <th>Last Name</th>
              <th>ID Number</th>
            </tr>
          </thead>
          <tbody>
            {/* Map over the sorted friends list and display each friend */}
            {friends.map((friend, index) => ( //for each friend in friends, generate a new row with first, last, and ID
              <tr key={index}>
                <td>{friend.firstName}</td> {/*Next 3 lines display first, last, and id of current friend in "friends" */}
                <td>{friend.lastName}</td>
                <td>{friend.idNumber}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <label>
        Search First Name:
        <input
          className="search-input"
          type="text"
          value={searchFirstName}
          onChange={(e) => setSearchFirstName(e.target.value)}
        />
      </label>
      <button className="submit-button" onClick={handleSearch}>
        Search
      </button>

      <p>{message}</p>
      {/* Button to navigate back to the authentication selection page */}
      <button onClick={handleGoBack}>
        Go Back to Authentication Selection
      </button>
    </div>
  );
};

export default AddFriendForm;

