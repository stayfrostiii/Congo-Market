
def compareParsed(str1, str2):
    return

# takes the string formatted as: name,tags,price
def parseItem(string):
    temp = str(string).split(",")
    parsedNameArr = temp[0].split(" ")
    parsedName = ""
    for wordName in parsedNameArr:
        parsedName += wordName + ";"
    
    fullParsed = parsedName + temp[1]

    parsedResult = [ fullParsed, temp[2] ]
    return parsedResult

# item_obj will hold an array of strings that will contain: name of item, tags, price
# The format will be end up being words separated by ";" and 
# keywords will hold an array of words separate by ";" given by the user
# The goal is to return a string with "array" of items to be printed 
# formatted as: name;itemkey,price|name;itemkey,price|...
def sortArr(item_obj, keywords):
    keywordDB = [""] * len(item_obj)
    keywords = ""
    for obj in item_obj:
        keywords += parseItem(obj)
    return 