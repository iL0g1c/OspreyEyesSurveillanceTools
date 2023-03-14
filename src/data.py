import json

def loadData():
    with open("data.json") as reader:
        if reader == None:
            reader = {}
        data = json.load(reader)
    return data

def saveData(data):
   with open("data.json", "w") as writer:
       writer.write(json.dumps(data))