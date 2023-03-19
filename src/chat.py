import jsonlines
from datetime import datetime
import urllib.parse

CATALOG_DIR = "catalog/"

def appendChat(chatData):
    with jsonlines.open(CATALOG_DIR + "chat.jsonl", mode="a") as writer:
        for message in chatData:
            writer.write(message)

def loadChat():
    chatData = []
    with jsonlines.open(CATALOG_DIR + "chat.jsonl") as reader:
        for obj in reader:
            chatData.append(obj)
    return chatData

def saveChat(chatData):
    with jsonlines.open(CATALOG_DIR + "chat.jsonl", "w") as writer:
        for message in chatData:
            writer.write(message)

def parseChat(messages):
    currentChatData = []
    msg = ""
    for message in messages:
        message["msg"] = urllib.parse.unquote(message["msg"])
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H-%M-%S")
        formated = {
            "acid": message["acid"],
            "msg": message["msg"],
            "time": date_str
        }
        currentChatData.append(formated)
        msg += f"{message['acid']}> {message['cs']}: {message['msg']}\n"
    appendChat(currentChatData)
    return msg