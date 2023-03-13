**DISCLAIMER: THIS SCRIPT IS IN BETA AND MAY NOT PERFORM AS EXPECTED.**
# GeoFS Callsign Tracker
### An OspreyEyes Creation

## How to run from release
1. Go to releases and download the windows 10 executable. (This only works on windows 10)
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
3. Run ```pyinstaller -n callsignTracker --onefile src/callsignTracker.py --distpath bin/```
4. Wait for build to finish.
5. Run the executable from the windows explorer.

_It is possible to use pyinstaller to build for another target OS, but this has not been tested._

## Rationale
In GeoFS MRP, people are constantly commiting FRP actions. Some of these include changing their callsign after being killed, and then rejoining the fight.
**This script will put an end to this.**

In GeoFS a user can change their callsign to anything that is available, but they can only change their account id by creating a new account.
Additionally, this script would be useful in figuring out spies in your force, as you can see their callsigns from other forces they are in.


## How Callsign Tracker Works
This callsign tracker uses the GeoFS map API to get all online users from the server.
Next, it checks every users callsign and account ID against what is currently in the database.
If it detects a changed callsign, it adds this to the database with all of that users previous callsigns.
This way you can tell if users are changing their callsigns, as you can see their previous callsigns.

## Problems
This does not completly stop callsign changes, as you can just create a new account to log in with. This will be a lot more difficult (email and phone number verification), but will hopefully cut down a lot of this type of FRP.
I have not tested running the script 24/7, and I suspect the preformance will degrade over time, as the extremely innificant "for loops" increase as the database grows. I would suggest only using this script during a specific time (Ex. A specific battle or dogfight). That way you can figure out changes when you need it most.
The user has to be online on GeoFS for their callsign to update in the database. If they change their callsign, but don't join the server, this script won't detect that. This shouldn't be a problem though, since they can't commit FRP while offline.
**Additionally, you will have to manually read the catalog.jsonl file in order to retrieve user data, since a GUI has yet to be implemented.**

## Planned Features
1. Porting to other Operating Systems besides Windows.
2. Improved performance
3. GUI to access callsign data

Feel free to suggest more ideas/bugs in the ideas tab.
