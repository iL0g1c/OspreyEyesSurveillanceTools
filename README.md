**DISCLAIMER: THIS SCRIPT IS IN BETA AND MAY NOT PERFORM AS EXPECTED.**
# Osprey Eyes Surveillance Tools
### An OspreyEyes Creation

## How to run from release
1. Go to releases and download the windows 10 executable for you chosen product. (This only works on windows 10)
2. Run executable.
3. The data log will be created in the same folder as the executable.

## How to run from source
### Run using python
1. Clone the repository.
2. You must have python installed on your machine.
3. You must install all packages for this script. Look in the code, since I am too lazy to create a requirements.txt file.
4. Run the script.

### Build from source
1. Clone the repository.
2. Install pyinstaller
3. Use the pyinstaller build command as outlined in pysinstaller documentation.
4. Wait for build to finish.
5. Run the executable from the windows explorer.

_It is possible to use pyinstaller to build for another target OS, but this has not been tested._

## Rationale
In GeoFS MRP, people are constantly commiting FRP actions. Some of these include changing their callsign after being killed, and then rejoining the fight.
**This script will put an end to this.**

In GeoFS a user can change their callsign to anything that is available, but they can only change their account id by creating a new account.
Additionally, this script would be useful in figuring out spies in your force, as you can see their callsigns from other forces they are in.


## How the Callsign Tracker Module Works
This callsign tracker uses the GeoFS map API to get all online users from the server.
Next, it checks every users callsign and account ID against what is currently in the database.
If it detects a changed callsign, it adds this to the database with all of that users previous callsigns.
This way you can tell if users are changing their callsigns, as you can see their previous callsigns.

## How the Chat Logger Module Works
This script is currently only available in the OspreyEyes bot, as the code is available elsewhere.
It pulls the recent chat messages from the multiplayer server, and then records them in a jsonlines file.
The original creator of this script is Ariakim Taiyo, but it was written in javascript and I rewrote it in python.

## Problems
1. This does not completly stop callsign changes, as you can just create a new account to log in with. This will be a lot more difficult (email and phone number verification), but will hopefully cut down a lot of this type of FRP.
2. The user has to be online on GeoFS for their callsign to update in the database. If they change their callsign, but don't join the server, this script won't detect that. This shouldn't be a problem though, since they can't commit FRP while offline.
3. The GUI is very basic/unstable, and the search algorithm does not work well.
4. In the beta there is no error catch system for the bot, and it can take up to 30 seconds for a command to fetch a response.

## Planned Features
1. Porting to other Operating Systems besides Windows.
2. Improved performance

Feel free to suggest more ideas/bugs in the ideas tab.
