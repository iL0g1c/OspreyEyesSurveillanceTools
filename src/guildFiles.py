import os
import jsonlines

CATALOG_DIR = "catalog/"

def loadGuildFile():
	foundGuildMatch = False
	if not os.path.exists(CATALOG_DIR + 'guilds.jsonl'):
		return (1, None)
	guildData = []
	with jsonlines.open(CATALOG_DIR + 'guilds.jsonl') as reader:
		for obj in reader:
			guildData.append(obj)
	return None, guildData


def saveGuildFile(guildData):
    with jsonlines.open(CATALOG_DIR + 'guilds.jsonl', mode='w') as writer:
        for guild in guildData:
            writer.write(guild)