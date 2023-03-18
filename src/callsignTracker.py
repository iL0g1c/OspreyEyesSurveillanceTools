import time
from callsigns import parseCallsigns
from map_api import get_users
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def guiRunner(stop_event):
	print("Starting Tracking...")
	while True:
		error, users = get_users()
		await parseCallsigns(users)
		if stop_event.is_set():
			print("Closed.")
			break
		time.sleep(1)

async def main():
	print("Starting Tracking...")
	while True:
		error, users = get_users()
		await parseCallsigns(users)
		time.sleep(1)

if __name__ in "__main__":
    asyncio.run(main())