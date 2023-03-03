import time
import os
from catalog import Catalog
from map_api import get_users

def setup():
	if not os.path.exists("catalog.jsonl"):
		with open("catalog.jsonl", "w") as fp:
			pass		

def main():
	setup()
	catalog = Catalog()
	print("Starting Tracking...")
	while True:
		users = get_users()
		catalog.parse(users)
		time.sleep(1)

if __name__ in "__main__":
    main()