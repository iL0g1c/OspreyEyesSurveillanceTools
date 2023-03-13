import requests
import json

def init_server_instance(geofs_session_id): # initializes connection and gains mandatory variables from server.
	# initializes server connection and gets details from server.
	body = {
		"origin": "https://www.geo-fs.com",
		"acid":"700485",
		"sid":geofs_session_id,
		"id":"",
		"ac":"1",
		"co":[42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
		"ve":[2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
		"st":{"gr":True,"as":0},
		"ti":1675268771889,
		"m":"", 
		"ci":0
	}
	try:
		response = requests.post(
			"https://mps.geo-fs.com/update",
			json = body,
			cookies = {"PHPSESSID": geofs_session_id}
		)
		print("Successfully connect to server.")
		response_body = json.loads(response.text)
		return response_body["myId"]
	except:
		print("Error code 1. Failed handshake.")

def sendMsg(myId, msg, geofs_session_id):
	body = {
		"origin": "https://www.geo-fs.com",
		"acid":"700485",
		"sid":geofs_session_id,
		"id":myId,
		"ac":"1",
		"co":[42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
		"ve":[2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
		"st":{"gr":True,"as":0},
		"ti":None,
		"m":msg,
		"ci": 0
	}
	try:
		response = requests.post(
			"https://mps.geo-fs.com/update",
			json = body,
			cookies = {"PHPSESSID": geofs_session_id}
		)
		response_body = json.loads(response.text)
		return response_body["myId"]
	except:
		print("Error code 2. Failed message sender.")