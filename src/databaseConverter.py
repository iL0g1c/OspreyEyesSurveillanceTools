from pymongo import MongoClient
from datetime import datetime
import os
import jsonlines
from bson import json_util


password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb://mongo_db_admin:password@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)
		
def loadCallsignFile():
	if not os.path.exists("callsigns.jsonl"):
		return 1, None
	callsignData = []
	with jsonlines.open("callsigns.jsonl") as reader:
		for obj in reader:
			callsignData.append(obj)
	return None, callsignData

def saveCallsignFile(callsignData):
	with jsonlines.open("callsigns.jsonl", mode = 'w') as writer:
		for item in callsignData:
			writer.write(item)

def string_to_datetime(string):
    datetime_obj = datetime.strptime(string, "%Y-%m-%d %H-%M-%S")
    return datetime_obj

def datetime_to_string(datetime_obj):
    datetime_str = datetime_obj.strftime("%Y-%m-%d %H-%M-%S")
    return datetime_str

def convertToMongoDB():
    database = client["OspreyEyes"]
    callsigns = database["callsigns"]
    error, callsignData = loadCallsignFile()
    callsignDocument = []
    for item in callsignData:
        callsignProcessedData = item
        for callsign in item["callsigns"]:
            for i in range(len(item["callsigns"][callsign])):
                processedTime = string_to_datetime(item["callsigns"][callsign][i])
                callsignProcessedData["callsigns"][callsign][i] = processedTime
        callsignDocument.append(callsignProcessedData)
    callsigns.insert_many(callsignDocument)

def convertToJson():
    database = client["OspreyEyes"]
    callsigns = database["callsigns"]
    documents = callsigns.find()
    callsignData = []

    print("Converting to json...")
    for document in documents:
        document_dict = json_util.loads(json_util.dumps(document))
        callsignData.append(document_dict)

    print("Processing Data...")
    finalData = []
    for item in callsignData:
        del item['_id']
        currentCallsignData = item
        for callsign in item["callsigns"]:
            for i in range(len(item["callsigns"][callsign])):
                processedTime = datetime_to_string(item["callsigns"][callsign][i])
                currentCallsignData["callsigns"][callsign][i] = processedTime
        finalData.append(currentCallsignData)

    print("Saving Data...")
    saveCallsignFile(finalData)



if __name__ in "__main__":
    convertToJson()