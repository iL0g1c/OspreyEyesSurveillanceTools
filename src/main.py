from operator import itemgetter
import requests
import json
import jsonlines
import time
from datetime import datetime
import os

def setup():
	if not os.path.exists("catalog.jsonl"):
		with open("catalog.jsonl", "w") as fp:
			pass

def get_users():
	try:
		response = requests.post(
			"https://mps.geo-fs.com/map",
			json = {
				"id":"",
				"gid": None
			}
		)
		response_body = json.loads(response.text)
		return response_body["users"]
	except:
		print("Error Code 0x1: Can not connect to GeoFS.")

def load_catalog():
	catalog = []
	with jsonlines.open("catalog.jsonl") as reader:
		for obj in reader:
			catalog.append(obj)

	return catalog

def save_catalog(catalog):
	with jsonlines.open("catalog.jsonl", mode = 'w') as writer:
		for item in catalog:
			writer.write(item)

def catalog(users):
	catalog = load_catalog()
	for user in users:
		match_check = False
		if user["acid"] != None and user["cs"] != "Foo" and user["cs"] != "":
			for item in catalog:
				if item["acid"] == user["acid"]:
					match_check = True
					if item["cur_callsign"] != user["cs"]:
						old_callsign = item["cur_callsign"]
						item["cur_callsign"] = user["cs"]
						
						now = datetime.now()
						date_str = now.strftime("%Y-%m-%d %H-%M-%S")
						cur_index = catalog.index(item)
						
						if user["cs"] not in item["callsigns"]:
							item["callsigns"][user["cs"]] = [date_str]
						else:
							item["callsigns"][user["cs"]].append(date_str)
						catalog[cur_index] = item
						print(f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}")
			if not match_check:
				now = datetime.now()
				date_str = now.strftime("%Y-%m-%d %H-%M-%S")
				catalog.append({
					"acid": int(user["acid"]),
					"cur_callsign": user["cs"],
					"callsigns": {user["cs"]: [date_str]}
				})
	save_catalog(catalog)
	
			
			

def main():
	setup()
	print("Starting Tracking...")
	while True:
		users = get_users()
		catalog(users)
		time.sleep(1)

if __name__ in "__main__":
    main()