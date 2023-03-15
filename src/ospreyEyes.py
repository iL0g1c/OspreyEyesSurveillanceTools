import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks, commands
from map_api import get_users
from catalog import parseCallsigns
from mutiplayer_api import init_server_instance, getMessages
from guildFiles import loadGuildFile, saveGuildFile
from data import saveData, loadData
from chat import parseChat

intents = discord.Intents.all()
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
geofs_session_id = os.getenv("GEOFS_SESSION_ID")
bot = commands.Bot(intents=intents, command_prefix="beta! ")
CATALOG_DIR = "catalog/"

def setup():
	if not os.path.exists(CATALOG_DIR):
		os.mkdir(CATALOG_DIR)
	if not os.path.exists(CATALOG_DIR + "callsigns.jsonl"):
		with open(CATALOG_DIR + "callsigns.jsonl", "w") as fp:
			pass
	if not os.path.exists(CATALOG_DIR + "guilds.jsonl"):
		with open(CATALOG_DIR + "guilds.jsonl", "w") as fp:
			pass
	if not os.path.exists(CATALOG_DIR + "chat.jsonl"):
		with open(CATALOG_DIR + "chat.jsonl", "w") as fp:
			pass
	if not os.path.exists(CATALOG_DIR + "data.json"):
		with open(CATALOG_DIR + "data.json", "w") as fp:
			fp.write("{}")
	return geofs_session_id

@tasks.loop(seconds=1)
async def printUsers(bot):
	users = get_users()[1]
	msg = parseCallsigns(users)

	error, guildData = loadGuildFile()
	for i in range(len(guildData)):
		if guildData[i]["callsignTrackerEnabled"]:
			channel = bot.get_channel(guildData[i]["callsignTrackerChannel"])
			if msg != "":
				await channel.send(discord.utils.escape_markdown(msg))
		

@tasks.loop(seconds=1)
async def printMessages(bot):
	data = loadData()
	myId, lastMsgId, messages = getMessages(data["myId"], geofs_session_id, data["lastMsgId"])
	data["lastMsgId"] = lastMsgId
	data["myId"] = myId
	saveData(data)
	msg = parseChat(messages)
	error, guildData = loadGuildFile()
	for i in range(len(guildData)):
		if guildData[i]["chatTrackerEnabled"]:
			channel = bot.get_channel(guildData[i]["chatTrackerChannel"])
			if msg != "":
				await channel.send(discord.utils.escape_markdown(msg))



@bot.event
async def on_ready():
	data = loadData()
	data["myId"], data["lastMsgId"] = init_server_instance(geofs_session_id, returnMyId=True)
	saveData(data)
	print("Bot has connected to discord.")
	printMessages.start(bot)
	printUsers.start(bot)

@bot.event
async def on_guild_join(guild):
	inDatabase = False
	print(f"OspreyEyes has been added to {guild.id}.\n Setting up...")
	error, guildData = loadGuildFile()

	for obj in guildData:
		if obj["id"] == guild.id:
			inDatabase = True

	if not inDatabase:
		guildData.append({
			"id": guild.id,
			"callsignTrackerChannel": None,
			"chatTrackerChannel": None,
			"callsignTrackerEnabled": False,
			"chatTrackerEnabled": False,

		})
	saveGuildFile(guildData)
	print("Setup successful.")

@bot.command(brief="Toggle callsign tracker on and off.", description="Toggle callsign tracker on and off.")
async def toggleCallsigns(ctx):
	await ctx.send("Toggling tracking...")
	error, guildData = loadGuildFile()
	for i in range(len(guildData)):
		if guildData[i]["id"] == ctx.message.guild.id:
			if guildData[i]["callsignTrackerEnabled"]:
				guildData[i]["callsignTrackerEnabled"] = False
				await ctx.send("Tracking terminated.")
			else:
				guildData[i]["callsignTrackerEnabled"] = True
				await ctx.send("Tracking started.")

	saveGuildFile(guildData)

@bot.command(brief="Toggle chat tracker on and off.", description="Toggle chat tracker on and off.")
async def toggleChat(ctx):
	await ctx.send("Toggling tracking...")
	error, guildData = loadGuildFile()

	for i in range(len(guildData)):
		if guildData[i]["id"] == ctx.message.guild.id:
			if guildData[i]["chatTrackerEnabled"]:
				guildData[i]["chatTrackerEnabled"] = False
				await ctx.send("Tracking terminated.")
			else:
				guildData[i]["chatTrackerEnabled"] = True
				await ctx.send("Tracking started.")
	saveGuildFile(guildData)

@bot.command(brief="Set callsign tracker channel.", description="Set callsign tracker channel.")
async def setChannel(ctx, trackerType, channel):
	error, guildData = loadGuildFile()
	for i in range(len(guildData)):
		if guildData[i]["id"] == ctx.message.guild.id:
			if trackerType == "callsign":
				guildData[i]["callsignTrackerChannel"] = int(channel)
			elif trackerType == "chat":
				guildData[i]["chatTrackerChannel"] = int(channel)
			await ctx.send(f"Binded the {trackerType} tracker to channel id: {channel}")
	saveGuildFile(guildData)

@bot.command(brief="Check connection.", description="Check connection.")
async def ping(ctx):
	delay = round(bot.latency * 1000)
	await ctx.send(f"PONG!\n {delay}ms")


if __name__ in "__main__":
	setup()
	bot.run(BOT_TOKEN)