import requests
import json

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