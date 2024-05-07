from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from models import Account, FriendModel

def add_friend_to_account(db: Session, friend: FriendModel, request: Request):
    # Simulate a user ID, you can replace this with an actual user ID from your database
    user_id = 1248606  # example hard-coded id number
    try:
        # Retrieve the account from the database using the provided user_id
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Initialize friends_list if it's None
        if account.friends_list is None:
            account.friends_list = ""

        # Check if friend with the same ID number already exists in the friends_list
        if friend.idNumber in account.friends_list.split(","):
            raise HTTPException(status_code=400, detail="Friend already in friends list")

        # Add the friend to the account's friends_list
        friends = account.friends_list.split(",")
        friend_details = f"{friend.idNumber}:{friend.firstName}:{friend.lastName}"
        friends.insert(0, friend_details)  # Insert at the beginning
        account.friends_list = ",".join(friends)

        db.commit()
        return {"message": "Friend added successfully"}
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

def delete_friend_from_account(db: Session, id_number: int, request: Request):
    user_id = 1248606  # Example hard-coded user ID
    try:
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Remove the friend from the account's friends_list
        friends = account.friends_list.split(",")   #splits friends_list into list of individual entries
        friends = [friend for friend in friends if friend.split(":")[0] != str(id_number)]  #filters our the column by finding id to be deleted
        account.friends_list = ",".join(friends)        #creates/joins the new list of people with the deleted/filtered friend removed

        db.commit()
        return {"message": "Friend deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

def fetch_friends_list(db: Session, request: Request):
   # Simulate a user ID, you can replace this with an actual user ID from your request
   user_id = 1248606  # example hard-coded id number
   try:
       # Retrieve the account from the database using the provided user_id
       account = db.query(Account).filter(Account.user_id == user_id).first()
       if not account:
           raise HTTPException(status_code=404, detail="Account not found")

       # Split the friends_list into individual friend details
       friends_list = account.friends_list.split(",")       #split entries in friends column by the comma
       friends = []                                     #initialize empty list called friends
       for friend_details in friends_list:      #for loop to iterate through entires
           if not friend_details:
               continue  # Skip empty strings
           print("Friend details:", friend_details)
           friend_info = friend_details.split(":")      #splits friend detailed between every comma by the colon ID:F:L
           if len(friend_info) != 3:                    #must have 3 elements per comma separated entry (ID:F:L)
               raise ValueError("Invalid friend details format")
           friend = {"idNumber": friend_info[0], "firstName": friend_info[1], "lastName": friend_info[2]}   #creates dictionary that maps values to respective names/keys
           friends.append(friend)       #add separated info to the friends list 

       return friends       #returns the array
   except Exception as e:
       print("Error:", e)
       raise HTTPException(status_code=500, detail="Internal server error")
   finally:
       db.close()
