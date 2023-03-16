import jsonlines
from datetime import datetime
import os

CATALOG_DIR = "catalog/"
		
def loadCallsignFile():
	if not os.path.exists(CATALOG_DIR + "callsigns.jsonl"):
		return 1, None
	callsignData = []
	with jsonlines.open(CATALOG_DIR + "callsigns.jsonl") as reader:
		for obj in reader:
			callsignData.append(obj)
	return None, callsignData

def saveCallsignFile(callsignData):
	with jsonlines.open(CATALOG_DIR + "callsigns.jsonl", mode = 'w') as writer:
		for item in callsignData:
			writer.write(item)

def parseCallsigns(users):
	error, callsignData = loadCallsignFile()
	msg = ""
	for user in users:
		match_check = False
		if user["acid"] != None and user["cs"] != "Foo" and user["cs"] != "":
			for item in callsignData:
				if item["acid"] == user["acid"]:
					match_check = True
					if item["cur_callsign"] != user["cs"]:
						old_callsign = item["cur_callsign"]
						item["cur_callsign"] = user["cs"]
						
						now = datetime.now()
						date_str = now.strftime("%Y-%m-%d %H-%M-%S")
						cur_index = callsignData.index(item)
						
						if user["cs"] not in item["callsigns"]:
							item["callsigns"][user["cs"]] = [date_str]
						else:
							item["callsigns"][user["cs"]].append(date_str)
						callsignData[cur_index] = item
						msg += f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}\n"
						print(f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}\n")
			if not match_check:
				now = datetime.now()
				date_str = now.strftime("%Y-%m-%d %H-%M-%S")
				callsignData.append({
					"acid": int(user["acid"]),
					"cur_callsign": user["cs"],
					"callsigns": {user["cs"]: [date_str]}
				})
	saveCallsignFile(callsignData)
	return msg