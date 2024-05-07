from sqlalchemy.orm import Session
from sqlalchemy import asc
from fastapi import HTTPException
from models import queryItem, getItemKey, addItem, searchItem, Item
from datetime import datetime
from search.searchAlgo import switch, sortArr

def isfloat(var):
    return isinstance(var, float)

def query_item(db: Session, item: queryItem):
    try:
        searchV = item.searchV.lower()
        preTag = switch(searchV)
        if (preTag != searchV):
            item_obj = db.query(Item).filter(Item.itemkey.like(f'%{preTag}%')).all()
        else:
            item_obj = db.query(Item).all()
        if item_obj is None:
            raise HTTPException(status_code=404, detail="Item not found")
        else:   
            temp = ""
            itemArr = ""
            counter = 0

            itemArr = sortArr(item_obj, searchV)

            # This for loop will call the parsing function and sort all of the queries by rating in itemArr
            for obj in item_obj:
                temp = obj.name + ";" + obj.itemkey + "," + str(obj.price) + "^" + str(obj.itemID) + "|" + temp
                counter = counter + 1
            return {"message" : itemArr, "counter" : counter, "tester" : temp}

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
            newIndex = 0
            if not item_obj:
                newIndex = 1 
            else:
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