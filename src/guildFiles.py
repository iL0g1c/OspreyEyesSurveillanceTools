import os
import jsonlines

def loadGuildFile(returnAllGuilds=False, guildID=None):
	foundGuildMatch = False
	if not os.path.exists('guilds.jsonl'):
		return (1, None)
	guildData = []
	with jsonlines.open('guilds.jsonl') as reader:
		for obj in reader:
			guildData.append(obj)
	if not returnAllGuilds:
		for guild in guildData:
			if guild['id'] == guildID:
				foundGuildMatch = True
				guildData = guild
				break
	if not foundGuildMatch:
		if returnAllGuilds:
			return None, guildData
		else:
			return 2, None
	else:
		return None, guildData


def saveGuildFile(guildData):
	with jsonlines.open('guilds.jsonl', mode='w') as writer:
		for guild in guildData:
			writer.write(guild)