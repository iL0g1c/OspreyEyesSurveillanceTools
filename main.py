from operator import itemgetter
import requests
import json
import jsonlines
import time


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
		print("connection error")

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
					if user["cs"] not in item["callsigns"]:
						cur_index = catalog.index(item)
						item["callsigns"].append(user["cs"])
						catalog[cur_index] = item
			if not match_check:
				catalog.append({
					"acid": int(user["acid"]),
					"callsigns": [user["cs"]]
				})
	save_catalog(catalog)
	
			
			

def main():
	while True:
		users = get_users()
		catalog(users)
		time.sleep(1)

if __name__ in "__main__":
    main()