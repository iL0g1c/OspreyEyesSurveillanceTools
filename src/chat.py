import jsonlines
from datetime import datetime

CATALOG_DIR = "catalog/"

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
    chatData = loadChat()
    msg = ""
    for message in messages:
        message["msg"] = message["msg"].replace("%20", " ")
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H-%M-%S")
        formated = {
            "acid": message["acid"],
            "msg": message["msg"],
            "time": date_str
        }
        chatData.append(formated)
        msg += f"{message['acid']}> {message['cs']}: {message['msg']}\n"
    saveChat(chatData)
    return msg