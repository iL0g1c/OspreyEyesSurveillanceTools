from pymongo import MongoClient
from datetime import datetime
import os
import jsonlines


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


def string_to_datetime(string):
    datetime_obj = datetime.strptime(string, "%Y-%m-%d %H-%M-%S")
    return datetime_obj

def convertDatabase():
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

if __name__ in "__main__":
    convertDatabase()