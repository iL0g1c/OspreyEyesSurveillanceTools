import time
import os
from catalog import parseCallsigns
from map_api import get_users

CATALOG_DIR = "catalog/"

def setup():
	if not os.path.exists(CATALOG_DIR):
		os.mkdir(CATALOG_DIR)
	if not os.path.exists(CATALOG_DIR + "callsigns.jsonl"):
		with open(CATALOG_DIR + "callsigns.jsonl", "w") as fp:
			pass

def guiRunner(stop_event):
	setup()
	print("Starting Tracking...")
	while True:
		error, users = get_users()
		if error:
			for i in range(10):
				print(f"Exiting tracker in... ({i+1})")
				time.sleep(1)
			break
		parseCallsigns(users)
		if stop_event.is_set():
			print("Closed.")
			break
		time.sleep(1)

def main():
	setup()
	print("Starting Tracking...")
	while True:
		error, users = get_users()
		if error:
			for i in range(10):
				print(f"Exiting in... ({i+1})")
				time.sleep(1)
			break
		parseCallsigns(users)
		time.sleep(1)

if __name__ in "__main__":
    main()