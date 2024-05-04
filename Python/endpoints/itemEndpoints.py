from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import queryItem, Item

def query_item(db: Session, item: queryItem):
    try:
        item_obj = db.query(Item).filter(Item.name == item.name).all()
        if item_obj is None:
            raise HTTPException(status_code=404, detail="Item not found")
        else:   
            message = [""] * len(item_obj)
            counter = 0
            for obj in item_obj:
                message[counter] = """
                    """ + obj.name + """, 
                    """ + obj.desc + """,
                    """ + str(obj.itemID) + """, 
                    """ + str(obj.price) + """, 
                    """ + str(obj.time) + """,
                    """ + str(obj.date) + ";"
                counter = counter + 1
                print(obj.name)
            return {"message" : message, "counter" : counter}

    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        # Log and handle other exceptions
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()