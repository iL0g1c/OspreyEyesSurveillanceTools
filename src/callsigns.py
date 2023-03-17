import jsonlines
from datetime import datetime
import os
import asyncio
import motor.motor_asyncio

password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb://mongo_db_admin:password@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)

database = client["OspreyEyes"]
callsigns = database["callsigns"]

async def update_callsign(user):
    query = {"acid": user["acid"]}
    accountData = await callsigns.find_one(query)
    if accountData:
        if accountData["cur_callsign"] != user["cs"]:
            old_callsign = accountData["cur_callsign"]
            accountData["cur_callsign"] = user["cs"]
            now = datetime.now()
            if user["cs"] not in accountData["callsigns"]:
                accountData["callsigns"][user["cs"]] = [now]
            else:
                accountData["callsigns"][user["cs"]].append(now)
            await callsigns.update_one(query, {'$set': accountData})
            print(f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}\n")
            return f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}\n"
    else:
        now = datetime.now()
        newAccountData = {
            "acid": int(user["acid"]),
            "cur_callsign": user["cs"],
            "callsigns": {user["cs"]: [now]}
        }
        await callsigns.insert_one(newAccountData)
        return ""

async def parseCallsigns(users):
    msg = ""
    tasks = []
    for user in users:
        if user["acid"] is not None and user["cs"] != "Foo" and user["cs"] != "":
            task = asyncio.create_task(update_callsign(user))
            tasks.append(task)
    results = await asyncio.gather(*tasks)
    msg = "".join([r for r in results if r])
    return msg