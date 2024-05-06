
from models import Item

class StrWRate:
    rating: int
    string: str

def compareParsed(str1, str2):
    return

# createKeywordStr will take a string and the keywords from the search to dissect and give a rating to the item
def createKeywordStr(string, searchKW):

    indexComma = str(string).index(",")
    indexPeriod = str(string).index(".")
    parsedString = string[:indexComma]

    return

# item_obj will hold an object that has the information
# The format will be end up being words separated by ";" and 
# keywords will hold an array of words separate by ";" given by the user
# The goal is to return a string with "array" of items to be printed 
# formatted as: name;itemkey,price|name;itemkey,price|...
def sortArr(item_obj, searchV):
    keywordDB = [] * len(item_obj)
    searchKW = str(searchV).split(" ")
    keywords = "lmao"
    for obj in item_obj:
        temp = obj.name + "," + obj.itemkey + "." + str(obj.price) + "^" + str(obj.itemID)
        keywordDB.append(createKeywordStr(temp, searchKW))
    return keywords

# Custom switch-case function since python doesn't have a built in version
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