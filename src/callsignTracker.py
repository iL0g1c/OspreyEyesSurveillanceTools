import time
import os
from catalog import Catalog
from map_api import get_users

def setup():
	if not os.path.exists("catalog.jsonl"):
		with open("catalog.jsonl", "w") as fp:
			pass

def guiRunner(stop_event):
	setup()
	catalog = Catalog()
	print("Starting Tracking...")
	while True:
		error, users = get_users()
		if error:
			for i in range(10):
				print(f"Exiting tracker in... ({i+1})")
				time.sleep(1)
			break
		catalog.parse(users)
		if stop_event.is_set():
			print("Closed.")
			break
		time.sleep(1)

def main():
	setup()
	catalog = Catalog()
	print("Starting Tracking...")
	while True:
		error, users = get_users()
		if error:
			for i in range(10):
				print(f"Exiting in... ({i+1})")
				time.sleep(1)
			break
		catalog.parse(users)
		time.sleep(1)

if __name__ in "__main__":
    main()