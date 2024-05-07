from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from models import Account, FriendModel

def add_friend_to_account(db: Session, user_id: int, friend: FriendModel, request: Request):
    # Simulate a user ID, you can replace this with an actual user ID from your database
    try:
        account = db.query(Account).filter(Account.user_id == user_id).first()  #assign variable account the queried account in the database
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")            #HTTP Exception if account does not exist

        if account.friends_list is None:                            # Initialize friends_list if it's None if the account has been found
            account.friends_list = ""               

        if friend.idNumber in account.friends_list.split(","):      #Split friends_list to see if ID exists           
            raise HTTPException(status_code=400, detail="Friend already in friends list")

        friends = account.friends_list.split(",")           #Add each entry in friends_list into friends list
        friend_details = f"{friend.idNumber}:{friend.firstName}:{friend.lastName}"  #f = f-string, special string that allows you to create unique strings
        friends.insert(0, friend_details)  # Insert at the beginning
        account.friends_list = ",".join(friends)        #insert back into column the friends list 

        db.commit()         #commit changes to database
        return {"message": "Friend added successfully"}
    except Exception as e:
        db.rollback()           #undo any change since last commit if there is exception
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

def delete_friend_from_account(db: Session, user_id: int, id_number: int):
    try:
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Remove the friend from the account's friends_list
        friends = account.friends_list.split(",")
        friends = [friend for friend in friends if friend.split(":")[0] != str(id_number)]
        account.friends_list = ",".join(friends)

        db.commit()
        return {"message": "Friend deleted successfully"}
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

def fetch_friends_list(db: Session, user_id: int):
    try:
        # Retrieve the account from the database using the provided user_id
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Split the friends_list into individual friend details
        friends_list = account.friends_list.split(",")
        friends = []
        for friend_details in friends_list:
            if not friend_details:
                continue
            friend_info = friend_details.split(":")
            if len(friend_info) != 3:
                raise ValueError("Invalid friend details format")
            friend = {"idNumber": friend_info[0], "firstName": friend_info[1], "lastName": friend_info[2]}
            friends.append(friend)

        return friends
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Account not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))  # Bad Request
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()