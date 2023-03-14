import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks, commands
from map_api import get_users
from catalog import Catalog
from mutiplayer_api import init_server_instance, getMessages
from guildFiles import loadGuildFile, saveGuildFile
from data import saveData, loadData
from chat import parseChat

intents = discord.Intents.all()
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN_BETA")
geofs_session_id = os.getenv("GEOFS_SESSION_ID")
bot = commands.Bot(intents=intents, command_prefix="osprey! ")

def setup():
	if not os.path.exists("callsigns.jsonl"):
		with open("callsigns.jsonl", "w") as fp:
			pass
	if not os.path.exists("guilds.jsonl"):
		with open("guilds.jsonl", "w") as fp:
			pass
	if not os.path.exists("chat.jsonl"):
		with open("chat.jsonl", "w") as fp:
			pass
	if not os.path.exists("data.json"):
		with open("data.json", "w") as fp:
			fp.write("{}")
	return geofs_session_id

@tasks.loop(seconds=1)
async def printUsers(catalog, channel):
	users = get_users()[1]
	catalog.parse(users)
	if catalog.msg != "":
		await channel.send(discord.utils.escape_markdown(catalog.msg))

@tasks.loop(seconds=1)
async def printMessages(channel):
	data = loadData()
	myId, lastMsgId, messages = getMessages(data["myId"], geofs_session_id, data["lastMsgId"])
	data["lastMsgId"] = lastMsgId
	data["myId"] = myId
	saveData(data)
	msg = parseChat(messages)
	if msg != "":
		await channel.send(discord.utils.escape_markdown(msg))



@bot.event
async def on_ready():
	data = loadData()
	data["myId"], data["lastMsgId"] = init_server_instance(geofs_session_id, returnMyId=True)
	saveData(data)
	print("Bot has connected to discord.")

@bot.event
async def on_guild_join(guild):
	inDatabase = False
	print(f"OspreyEyes has been added to {guild.id}.\n Setting up...")
	error, guildData = loadGuildFile(returnAllGuilds=True)

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
	error, guildData = loadGuildFile(guildID = ctx.message.guild.id)
	channel = bot.get_channel(guildData["callsignTrackerChannel"])
	
	catalog = Catalog()

	if guildData["callsignTrackerEnabled"]:
		printUsers.cancel()
		guildData["callsignTrackerEnabled"] = False
		await channel.send("Tracking terminated.")
	else:
		printUsers.start(catalog, channel)
		guildData["callsignTrackerEnabled"] = True
		await channel.send("Trackign started.")

	saveGuildFile([guildData])

@bot.command(brief="Toggle chat tracker on and off.", description="Toggle chat tracker on and off.")
async def toggleChat(ctx):
	error, guildData = loadGuildFile(guildID = ctx.message.guild.id)
	channel = bot.get_channel(guildData["chatTrackerChannel"])

	if guildData["chatTrackerEnabled"]:
		printMessages.cancel()
		guildData["chatTrackerEnabled"] = False
		await channel.send("Tracking terminated.")
	else:
		printMessages.start(channel)
		guildData["chatTrackerEnabled"] = True
		await channel.send("Tracking started.")
	saveGuildFile([guildData])

@bot.command(brief="Set callsign tracker channel.", description="Set callsign tracker channel.")
async def setChannel(ctx, trackerType, channel):
	error, guildData = loadGuildFile(guildID = ctx.message.guild.id)
	if trackerType == "callsign":
		guildData["callsignTrackerChannel"] = int(channel)
	elif trackerType == "chat":
		guildData["chatTrackerChannel"] = int(channel)
	saveGuildFile([guildData])
	await ctx.send(f"Binded the {trackerType} tracker to channel id: {channel}")


@bot.command(brief="Check connection.", description="Check connection.")
async def ping(ctx):
	delay = round(bot.latency * 1000)
	await ctx.send(f"PONG!\n {delay}ms")


if __name__ in "__main__":
	setup()
	bot.run(BOT_TOKEN)