import discord
import json

# UPDATE THIS WHEN ADDING NEW PREFS
keyNum = 7

async def addServerIfNeeded(server, bot):
	sid = server.id
	try:
		await bot.pg_con.fetch("SELECT * FROM serverprefs WHERE serverid = $1", sid)
		return True
	except: # if server doesn't exist in table
		await bot.pg_con.execute("INSERT INTO serverprefs (wchnl, arole1, arole2, arole3, arole4, arole5, prefix, serverid) VALUES (general,NULL,NULL,NULL,NULL,NULL,!, $1)", sid)
		return False



async def getPfx(server, bot):
	sid = str(server.id)
	srow = await bot.pg_con.fetch("SELECT prefix FROM serverprefs WHERE serverid = $1", sid)
	return srow