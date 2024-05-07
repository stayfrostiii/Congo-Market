
from models import Item
import re

class StrWRate:
    def __init__(self, rating: int, string: str):
        self.rating = rating
        self.string = string

    def __str__(self):
        return f"{self.string} - {self.rating} @ "

class TreeNode(object):
    def __init__(self, value: StrWRate):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

# AVL tree class which supports the  
# Insert operation 
class AVLTree(object): 
  
    def insert(self, node: TreeNode, inserted): 
      
        # Step 1 - Adds to tree
        if not node: 
            return TreeNode(inserted) 
        elif inserted.rating < node.value.rating: 
            node.left = self.insert(node.left, inserted) 
        else: 
            node.right = self.insert(node.right, inserted) 
  
        # Step 2 - Update the height of the each Node traversed through when inserting 
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right)) 
  
        # Step 3 - Get balance factor of each Node traversed through when inserting
        balance = self.getBalance(node) 
  
        # Step 4 - If Node is unbalanced, then test 4 cases
        # Case 1 - Left Left 
        if balance > 1 and inserted.rating < node.left.value.rating: 
            return self.rightRotate(node) 
  
        # Case 2 - Right Right 
        if balance < -1 and inserted.rating > node.right.value.rating: 
            return self.leftRotate(node) 
  
        # Case 3 - Left Right 
        if balance > 1 and inserted.rating > node.left.value.rating: 
            node.left = self.leftRotate(node.left) 
            return self.rightRotate(node) 
  
        # Case 4 - Right Left 
        if balance < -1 and inserted.rating < node.right.value.rating: 
            node.right = self.rightRotate(node.right) 
            return self.leftRotate(node) 
  
        return node 
  

    # Rotate parent node and make it left child node of current child of parent
    def leftRotate(self, parent: TreeNode): 
  
        # Rotate nodes ( (C)<-(B)<-(A) to (C)<-(B)->(A) )
        child = parent.right 
        temp = child.left 
        child.left = parent 
        parent.right = temp 
  
        # Update heights 
        parent.height = 1 + max(self.getHeight(parent.left), self.getHeight(parent.right)) 
        child.height = 1 + max(self.getHeight(child.left), self.getHeight(child.right)) 
  
        # Return new "parent" 
        return child 
  
    # Rotate parent node and make it right child node of current child of parent
    def rightRotate(self, parent: TreeNode): 
  
        # Rotate nodes  ( (A)->(B)->(C) to (A)<-(B)->(C) )
        child = parent.left 
        temp = child.right 
        child.right = parent 
        parent.left = temp 
  
        # Update heights 
        parent.height = 1 + max(self.getHeight(parent.left), self.getHeight(parent.right)) 
        child.height = 1 + max(self.getHeight(child.left), self.getHeight(child.right)) 
  
        # Return new "parent" 
        return child 
  
    def getHeight(self, node: TreeNode): 
        if not node: 
            return 0
        return node.height 
  
    def getBalance(self, node: TreeNode): 
        if not node: 
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right) 

    def inOrderToStr(self, node: TreeNode):
        temp = ""
        result = self.inOrderHelper(node, temp)
        return result

    def inOrderHelper(self, node: TreeNode, result):

        if not node:
            return ""
        resultR = self.inOrderHelper(node.right, result)
        resultM = node.value.string
        resultL = self.inOrderHelper(node.left, result)
        return resultR + resultM + resultL

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

    print(parsedTotal)

    rating = 0
    excluded = ["a","about","actually","almost","also","although","always","am","an","and","any",
                "are","as","at","be","became","become","but","by","can","could","did","do","does",
                "each","either","else","for","from","had","has","have","hence","how","i","if","in",
                "is","it","its","just","may","maybe","me","might","mine","must","my","neither","nor",
                "not","of","oh","ok","when","where","whereas","wherever","whenever","whether","which",
                "while","who","whom","whoever","whose","why","will","with","within","without","would",
                "yes","yet","you","your"]

    for word in parsedTotal:
        word = word.lower()
        print(word + " - " + searchV)
        if ( searchV in word or word in searchV ) and not word in excluded: 
            rating += 4
            print("+1")
        if (obj.pageVisits != 0):
            rating = rating * obj.pageVisits

    return rating

# item_obj will hold an object that has the information
# The format will be end up being words separated by ";" and 
# keywords will hold an array of words separate by ";" given by the user
# The goal is to return a string with "array" of items to be printed 
# formatted as: name;itemkey,price|name;itemkey,price|...
def sortArr(item_obj, searchV: str):
    
    avl = AVLTree()
    root = None

    keywords = ""
    for obj in item_obj:
        strToPrint = obj.name + ";" + obj.itemkey + "," + str(obj.price) + "^" + str(obj.itemID) + "|"
        rating = findRating(obj, searchV)
        item = StrWRate(rating, strToPrint)

        keywords += obj.name + ": " + str(rating) + " | "

        # temper = str(obj.desc).split(" ")
        # for words in temper:
        #     keywords += words + ","
        # keywords += " ---- "

        root = avl.insert(root, item)

    result = avl.inOrderToStr(root)
    return result

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