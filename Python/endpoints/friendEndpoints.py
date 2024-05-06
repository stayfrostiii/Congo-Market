from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from models import Account, FriendModel

def add_friend_to_account(db: Session, friend: FriendModel, request: Request):
    # Simulate a user ID, you can replace this with an actual user ID from your database

    #user_id = request.cookies.get("user_id")
    user_id = 1486774 #example hard-coded id number
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
        friends.insert(0, friend.idNumber)  # Insert at the beginning
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
    user_id = 1486774  # Example hard-coded user ID
    try:
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Remove the friend from the account's friends_list
        friends = account.friends_list.split(",")
        if str(id_number) not in friends:
            raise HTTPException(status_code=404, detail="Friend not found in friends list")
        friends.remove(str(id_number))
        account.friends_list = ",".join(friends)

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


"""
def delete_friend_from_account(db: Session, id_number: int, request: Request):
    # Simulate a user ID, you can replace this with an actual user ID from your database
    #user_id = request.cookies.get("user_id")
    user_id = 1909546 #example hard-coded id number
    try:
        # Retrieve the account from the database using the provided user_id
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Check if friend with the provided ID number exists in the friends_list
        if str(id_number) not in account.friends_list.split(","):
            raise HTTPException(status_code=400, detail="Friend not found in friends list")

        # Remove the friend from the account's friends_list
        friends = account.friends_list.split(",")
        friends.remove(str(id_number))
        account.friends_list = ",".join(friends)

        db.commit()
        return {"message": "Friend removed successfully"}
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


def delete_friend_from_account(db: Session, friend: FriendModel, request: Request):
    # Simulate a user ID, you can replace this with an actual user ID from your database
    #user_id = request.cookies.get("user_id")
    user_id = 1909546  # example hard-coded id number
    try:
        # Retrieve the account from the database using the provided user_id
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Check if friend with the provided ID number exists in the friends_list
        if friend.idNumber not in account.friends_list.split(","):
            raise HTTPException(status_code=400, detail="Friend not found in friends list")

        # Remove the friend from the account's friends_list
        friends = account.friends_list.split(",")
        friends.remove(friend.idNumber)
        account.friends_list = ",".join(friends)

        db.commit()
        return {"message": "Friend deleted successfully"}
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()
"""
