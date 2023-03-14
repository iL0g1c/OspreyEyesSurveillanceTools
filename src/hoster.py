import time
import os
from dotenv import load_dotenv
from map_api import get_users
from catalog import Catalog
from mutiplayer_api import init_server_instance, sendMsg

def setup():
	load_dotenv()
	geofs_session_id = os.getenv("GEOFS_SESSION_ID")
	if not os.path.exists("callsigns.jsonl"):
		with open("callsigns.jsonl", "w") as fp:
			pass
	return geofs_session_id

def main():
	geofs_session_id = setup()
	myId = init_server_instance(geofs_session_id)
	catalog = Catalog()
	print("Starting Tracking...")
	while True:
		users = get_users()[1]
		catalog.parse(users)
		if catalog.msg != "":
			myId = sendMsg(myId, catalog.msg, geofs_session_id)
		time.sleep(1)
if __name__ in "__main__":
	main()