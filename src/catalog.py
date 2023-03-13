from typing_extensions import Self
import jsonlines
from datetime import datetime
import os

class Catalog:
	def __init__(self):
		self.catalog = []
		self.msg = ""
		
	def load_catalog(self):
		if not os.path.exists("catalog.jsonl"):
			return 1
		self.catalog = []
		with jsonlines.open("catalog.jsonl") as reader:
			for obj in reader:
				self.catalog.append(obj)

	def save_catalog(self):
		with jsonlines.open("catalog.jsonl", mode = 'w') as writer:
			for item in self.catalog:
				writer.write(item)

	def parse(self, users):
		self.msg = ""
		self.load_catalog()
		cur_catalog = self.catalog
		for user in users:
			match_check = False
			if user["acid"] != None and user["cs"] != "Foo" and user["cs"] != "":
				for item in cur_catalog:
					if item["acid"] == user["acid"]:
						match_check = True
						if item["cur_callsign"] != user["cs"]:
							old_callsign = item["cur_callsign"]
							item["cur_callsign"] = user["cs"]
						
							now = datetime.now()
							date_str = now.strftime("%Y-%m-%d %H-%M-%S")
							cur_index = cur_catalog.index(item)
						
							if user["cs"] not in item["callsigns"]:
								item["callsigns"][user["cs"]] = [date_str]
							else:
								item["callsigns"][user["cs"]].append(date_str)
							cur_catalog[cur_index] = item
							self.msg += f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}\n"
							print(f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}\n")
				if not match_check:
					now = datetime.now()
					date_str = now.strftime("%Y-%m-%d %H-%M-%S")
					cur_catalog.append({
						"acid": int(user["acid"]),
						"cur_callsign": user["cs"],
						"callsigns": {user["cs"]: [date_str]}
					})
		self.catalog = cur_catalog
		self.save_catalog()