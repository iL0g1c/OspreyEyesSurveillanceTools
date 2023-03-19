import json

CATALOG_DIR = "catalog/"

def loadData():
    with open(CATALOG_DIR + "data.json") as reader:
        if reader == None:
            reader = {}
        data = json.load(reader)
    return data

def saveData(data):
   with open(CATALOG_DIR + "data.json", "w") as writer:
       writer.write(json.dumps(data))