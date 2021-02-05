import discord
import json

# UPDATE THIS WHEN ADDING NEW PREFS
keyNum = 7

async def checkKeys(server):
	with open('serverprefs.json', 'r') as s:
		sjson = json.load(s)

	sid = str(server.id)
	try:
		if len(sjson[sid]) < keyNum:
			wmsgB = sjson[sid]['wmsg']
			arole1B = sjson[sid]['arole1']
			arole2B = sjson[sid]['arole2']
			arole3B = sjson[sid]['arole3']
			arole4B = sjson[sid]['arole4']
			arole5B = sjson[sid]['arole5']
			if 'prefix' in sjson[sid]:
				prefixB = sjson[sid]['prefix']
			else:
				prefixB = "!"
			sjson[sid] = {}
			sjson[sid]['wmsg'] = wmsgB
			sjson[sid]['arole1'] = arole1B
			sjson[sid]['arole2'] = arole2B
			sjson[sid]['arole3'] = arole3B
			sjson[sid]['arole4'] = arole4B
			sjson[sid]['arole5'] = arole5B
			sjson[sid]['prefix'] = prefixB

			del sjson[sid]
	except: # if server not in json
		wmsgB = ""
		arole1B = ""
		arole2B = ""
		arole3B = ""
		arole4B = ""
		arole5B = ""
		prefixB = "!"
		sjson[sid] = {}
		sjson[sid]['wmsg'] = wmsgB
		sjson[sid]['arole1'] = arole1B
		sjson[sid]['arole2'] = arole2B
		sjson[sid]['arole3'] = arole3B
		sjson[sid]['arole4'] = arole4B
		sjson[sid]['arole5'] = arole5B
		sjson[sid]['prefix'] = prefixB

	with open('serverprefs.json', 'w') as s:
		json.dump(sjson, s)

async def addServerIfNeeded(sjson, server):
	sid = int(server.id)
	if sid not in sjson:
		sjson[sid] = {}
		sjson[sid]['wmsg'] = ''
		sjson[sid]['arole1'] = ''
		sjson[sid]['arole2'] = ''
		sjson[sid]['arole3'] = ''
		sjson[sid]['arole4'] = ''
		sjson[sid]['arole5'] = ''
		sjson[sid]['prefix'] = '!'
		return True
	else:
		return False

async def getPfx(server):
	with open('serverprefs.json', 'r') as s:
		sjson = json.load(s)

	sid = str(server.id)

	with open('serverprefs.json', 'w') as s:
		json.dump(sjson, s)

	return sjson[sid]['prefix']