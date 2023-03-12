import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks, commands
from map_api import get_users
from catalog import Catalog
from mutiplayer_api import init_server_instance

intents = discord.Intents.all()
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
geofs_session_id = os.getenv("GEOFS_SESSION_ID")
bot = commands.Bot(intents=intents, command_prefix="osprey! ")

def setup():
	if not os.path.exists("catalog.jsonl"):
		with open("catalog.jsonl", "w") as fp:
			pass
	return geofs_session_id

@tasks.loop(seconds=1)
async def printUsers(catalog, channel):
	users = get_users()[1]
	catalog.parse(users)
	if catalog.msg != "":
		await channel.send(discord.utils.escape_markdown(catalog.msg))

@bot.event
async def on_ready():
	channel = bot.get_channel(1084151674907668591)
	myId = init_server_instance(geofs_session_id)
	catalog = Catalog()
	await channel.send("Starting Tracking...")
	printUsers.start(catalog, channel)


@bot.command(brief="Check connection.", description="Check connection.")
async def ping(ctx):
	delay = round(bot.latency * 1000)
	await ctx.send(f"PONG!\n {delay}ms")

bot.run(BOT_TOKEN)