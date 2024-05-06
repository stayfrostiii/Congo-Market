
from models import Item
import re

class TreeNode(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

# class AVL_Tree(object):
#     def insert(self, root, key):

        


class StrWRate:
    def __init__(self, rating: int, string: str):
        self.rating = rating
        self.string = string

# createKeywordStr will take a string and the keywords from the search to dissect and give a rating to the item
# Return an item of type StrWRate, which will hold string to print and rating
def findRating(obj, searchV):

    unparsedName = obj.name
    unparsedTags = obj.tags
    unparsedDesc = obj.desc

    parsedName = str(unparsedName).split(" ")
    parsedTags = str(unparsedTags).split(";")
    parsedDesc = str(unparsedDesc).split(" ")

    parsedTotal = parsedTags
    parsedTotal += parsedName
    parsedTotal += parsedDesc

    rating = 0

    for word in parsedTotal:
        if searchV in word or word in searchV: 
            rating += 1

    return rating

# item_obj will hold an object that has the information
# The format will be end up being words separated by ";" and 
# keywords will hold an array of words separate by ";" given by the user
# The goal is to return a string with "array" of items to be printed 
# formatted as: name;itemkey,price|name;itemkey,price|...
def sortArr(item_obj, searchV: str):
    keywordDB = []
    keywords = ""
    for obj in item_obj:
        strToPrint = obj.name + ";" + obj.itemkey + "," + str(obj.price) + "^" + str(obj.itemID) + "|"
        rating = findRating(obj, searchV)
        item = StrWRate(rating, strToPrint)
        keywordDB.append(item)
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