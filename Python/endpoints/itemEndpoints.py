from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import queryItem, getItemID, Item

def query_item(db: Session, item: queryItem):
    try:
        item_obj = db.query(Item).filter(Item.name.like(f'%{item.name}%')).all()
        if item_obj is None:
            raise HTTPException(status_code=404, detail="Item not found")
        else:   
            temp = ""
            counter = 0
            for obj in item_obj:
                temp = obj.name + "," + str(obj.price) + ";" + str(obj.itemID) + "|" + temp
                counter = counter + 1
            return {"message" : temp + "@", "counter" : counter}

    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        # Log and handle other exceptions
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


def item_profile(db: Session, item: getItemID):
    try:
        item_obj = db.query(Item).filter(Item.itemID == item.itemID).all()
        if item_obj is None:
            raise HTTPException(status_code=404, detail="Item not found")
        else:   
            message = [""] * len(item_obj)
            temp = ""
            for obj in item_obj:
                temp = (obj.itemkey + "," + 
                        obj.name + "." +
                        obj.desc + ";" +
                        str(obj.itemID) + ":" +
                        str(obj.price) + "!" +
                        str(obj.time) + "@" + 
                        str(obj.date) + "|" +
                        str(obj.owner) + "$" +
                        str(obj.distCenter) + "&")
            return {"message" : temp}

    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        # Log and handle other exceptions
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()