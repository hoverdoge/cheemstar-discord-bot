import discord
import json

# UPDATE THIS WHEN ADDING NEW PREFS
keyNum = 7

async def addServerIfNeeded(server, bot):
	sid = str(server.id)
	serverObj = await bot.pg_con.fetch("SELECT * FROM serverprefs WHERE serverid = $1", sid)
	if not serverObj:  # if server doesn't exist in table
		await bot.pg_con.execute("INSERT INTO serverprefs (wchnl, arole1, arole2, arole3, arole4, arole5, prefix, serverid) VALUES ('general',' ',' ',' ',' ',' ','!', $1)", sid)



async def getPfx(server, bot):
	sid = str(server.id)
	srow = await bot.pg_con.fetchrow("SELECT * FROM serverprefs WHERE serverid = $1", sid)
	prefix = str(srow['prefix'])
	return str(prefix)