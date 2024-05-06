from sqlalchemy.orm import Session
from sqlalchemy import asc
from fastapi import HTTPException
from models import queryItem, getItemKey, addItem, searchItem, Item
from datetime import datetime
# from search.searchAlgo import sortArr

def isfloat(var):
    return isinstance(var, float)

def switch(argument):
    if argument == "": return argument
    if (argument in "book" or 
        argument in "movie" or 
        "book" in argument or 
        "movie" in argument
        ): return "a"
    if (argument in "electronics" or
        "electronic" in argument
        ): return "b"
    if (argument in "computers" or
        "computer" in argument
        ): return "c"
    if (argument in "garden" or 
        argument in "tools" or 
        "garden" in argument or 
        "tool" in argument
        ): return "d"
    if (argument in "beauty" or 
        argument in "health" or 
        "beauty" in argument or 
        "health" in argument
        ): return "e"
    if (argument in "toys" or
        "toy" in argument
        ): return "f"
    if (argument in "handmade" or
        "handmade" in argument
        ): return "g"
    if (argument in "sports" or 
        argument in "outdoors" or 
        "sport" in argument or 
        "outdoor" in argument
        ): return "h"
    if (argument in "automotive" or 
        argument in "industrial" or 
        "automotive" in argument or 
        "industrial" in argument
        ): return "i"
    if (argument in "collectibles" or
        "collectible" in argument
        ): return "j"
    else: return argument

def query_item(db: Session, item: queryItem):
    try:
        searchV = item.searchV.lower()
        result = switch(searchV)
        if (result != searchV):
            item_obj = db.query(Item).filter(Item.itemkey.like(f'%{result}%')).all()
        else:
            item_obj = db.query(Item).all()
        if item_obj is None:
            raise HTTPException(status_code=404, detail="Item not found")
        else:   
            temp = ""
            unparsedArr = [""] * len(item_obj)
            counter = 0
            for obj in item_obj:

                temp = obj.name + ";" + obj.itemkey + "," + str(obj.price) + "^" + str(obj.itemID) + "|" + temp
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


def item_profile(db: Session, item: getItemKey):
    try:
        item_obj = db.query(Item).filter(Item.itemID == item.itemID).all()
        if item_obj is None:
            raise HTTPException(status_code=404, detail="Item not found")
        else:   
            temp = [""] * 10
            for obj in item_obj:
                temp[0] = obj.itemkey
                temp[1] = obj.name
                temp[2] = obj.desc
                temp[3] = obj.itemID
                temp[4] = obj.price
                temp[5] = obj.time
                temp[6] = obj.date
                temp[7] = obj.owner
                temp[8] = obj.distCenter
                temp[9] = obj.tags
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

def add_item(db: Session, item: addItem):
    try:
        if (isfloat(float(item.price))):
            item_obj = db.query(Item).order_by(asc(Item.itemID)).all()
            obj = item_obj.pop()
            newIndex = obj.itemID + 1
            currentDT = datetime.now()
            currentDTStr = str(currentDT)
            currentDate = currentDTStr[:10]
            currentTime = currentDTStr[12:19]

            firstTag = item.tags.split(';')

            ikey = firstTag[0] + str(newIndex)

            new_item = Item(
                itemkey=ikey, 
                name=item.name,
                tags=item.tags, 
                desc=item.desc, 
                itemID=newIndex, 
                price=float(item.price),
                date = currentDate,
                time = currentTime
                )
            db.add(new_item)
            db.commit()
            return {"message" : "successfully added"}
        else:
            raise HTTPException(status_code=400, detail="Price not integer")

    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        db.rollback()
        # Log and handle other exceptions
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

def search_item(db: Session, item: searchItem):
    try:
        item_obj = db.query(Item).filter(Item.itemkey[0] == item.itemkey[0]).all()
        if item_obj is None:
            raise HTTPException(status_code=404, detail="Item not found")
        else:   
            temp = [""] * 10
            for obj in item_obj:
                temp[0] = obj.itemkey
                temp[1] = obj.name
                temp[2] = obj.desc
                temp[3] = obj.itemID
                temp[4] = obj.price
                temp[5] = obj.time
                temp[6] = obj.date
                temp[7] = obj.owner
                temp[8] = obj.distCenter
                temp[9] = obj.tags
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