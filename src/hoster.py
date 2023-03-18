import time
import os
from dotenv import load_dotenv
import asyncio
from map_api import get_users
from callsigns import parseCallsigns
from mutiplayer_api import init_server_instance, sendMsg

load_dotenv()
geofs_session_id = os.getenv("GEOFS_SESSION_ID")

async def main():
	myId = init_server_instance(geofs_session_id)

	print("Starting Tracking...")
	while True:
		users = get_users()[1]
		msg = await parseCallsigns(users)
		if msg != "":
			myId = sendMsg(myId, msg, geofs_session_id)
		time.sleep(1)
if __name__ in "__main__":
	asyncio.run(main())