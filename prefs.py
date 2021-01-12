import discord

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