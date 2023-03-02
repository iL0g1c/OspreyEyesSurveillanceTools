# GeoFS Callsign Tracker
### An OspreyEyes Creation

## How to Use
1. You must have python installed on your machine.
2. You must install all packages for this script. Look in the code, since I am too lazy to create a requirements.txt file.
3. Run the script.

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

## Planned Features
1. Time stamps for when the callsigns are changed.
2. Improved performance

Feel free to suggest more ideas/bugs in the ideas tab.
