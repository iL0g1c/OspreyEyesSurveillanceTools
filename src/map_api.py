import requests
import json
import time

def get_users():
	for i in range(10):
		try:
			response = requests.post(
				"https://mps.geo-fs.com/map",
				json = {
					"id":"",
					"gid": None
				}
			)
			response_body = json.loads(response.text)
			return None, response_body["users"]
		except:
			print("Error Code 0x1: Can not connect to GeoFS.")
			print(f"Retrying... ({i+1})")
			time.sleep(1)
			continue
	print("Unable to connect to GeoFS. Check your connection and restart the application.")
	return 2, None