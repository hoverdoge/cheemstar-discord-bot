from discord.ext import commands
import json
import discord
import prefs

class Settings(commands.Cog):
	"""setup, welcomechannel"""
	def __init__(self, bot):
		self.bot = bot
	### SETUP ###
	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def botsetup(self, ctx):
		"""Can only be used once. Shows commands to setup bot"""
		with open('serverprefs.json', 'r') as s:
			serverprefs = json.load(s)
		########################################
		newserver = await prefs.addServerIfNeeded(serverprefs, ctx.message.channel.guild)
		### if the server is new, do setup
		if newserver == False:
			await ctx.message.channel.send("This server has already gone through setup!")
		else:
			await ctx.message.channel.send("Setup commands: `!welcomechannel, !autorole, !prefix'")
		########################################
		with open('serverprefs.json', 'w') as s:
			json.dump(serverprefs, s)

	### WELCOME CHANNEL ###
	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def welcomechannel(self, ctx):
		"""`!welcomechannel` - channel welcome messages are sent in - requires admin"""
		with open('serverprefs.json', 'r') as s:
			serverprefs = json.load(s)
		########################################
		sid = ctx.message.guild.id
		channel = ctx.message.channel
		await channel.send("Welcome messages will now be sent to `" + str(channel) + "`")
		serverprefs[str(sid)]['wmsg'] = channel.id
		########################################
		with open('serverprefs.json', 'w') as s:
			json.dump(serverprefs, s)

	### WELCOME CHANNEL ###
	@commands.command()
	@commands.has_permissions(manage_roles=True) 
	async def autorole(self, ctx, role):
		"""`!autorole ROLE` - gives new members a certain role (up to 5 addable) - requires manage roles"""
		with open('serverprefs.json', 'r') as s:
			serverprefs = json.load(s)
		########################################
		svr = str(ctx.message.guild.id)

		if serverprefs[svr]['arole1'] == "":
			serverprefs[svr]['arole1'] = role
			await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
		elif serverprefs[svr]['arole2'] == "":
			serverprefs[svr]['arole2'] = role
			await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
		elif serverprefs[svr]['arole3'] == "":
			serverprefs[svr]['arole3'] = role
			await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
		elif serverprefs[svr]['arole4'] == "":
			serverprefs[svr]['arole4'] = role
			await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
		elif serverprefs[svr]['arole5'] == "":
			serverprefs[svr]['arole5'] = role
			await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
		else:
			await ctx.message.channel.send("You already have 5 roles. Your autorole list has been cleared.")
			serverprefs[svr]['arole1'] = ""
			serverprefs[svr]['arole2'] = ""
			serverprefs[svr]['arole3'] = ""
			serverprefs[svr]['arole4'] = ""
			serverprefs[svr]['arole5'] = ""
 

		########################################
		with open('serverprefs.json', 'w') as s:
			json.dump(serverprefs, s)

	@commands.command()
	async def autorolelist(self, ctx):
		"""`!autorolelist` - lists all roles given automatically to new members"""
		with open('serverprefs.json', 'r') as s:
			serverprefs = json.load(s)
		########################################
		svr = str(ctx.message.guild.id)
		role1 = "None"
		role2 = "None"
		role3 = "None"
		role4 = "None"
		role5 = "None"

		if serverprefs[svr]['arole1'] != "":
			role1 = serverprefs[svr]['arole1']
		if serverprefs[svr]['arole2'] != "":
			role2 = serverprefs[svr]['arole2']
		if serverprefs[svr]['arole3'] != "":
			role3 = serverprefs[svr]['arole3']
		if serverprefs[svr]['arole4'] != "":
			role4 = serverprefs[svr]['arole4']
		if serverprefs[svr]['arole5'] != "":
			role5 = serverprefs[svr]['arole5']
		embed = discord.Embed(
			title = "List of Automatically Assigned Roles",
			description = "Role 1: `" + role1 + "`\nRole 2: `" + role2 + "`\nRole 3: `" + role3 + "`\nRole 4: `" + role4 + "`\nRole 5: `" + role5 + "`",
			colour = discord.Colour.blue()
			)
		await ctx.message.channel.send(embed=embed)


		########################################
		with open('serverprefs.json', 'w') as s:
			json.dump(serverprefs, s)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def prefix(self, ctx, prefix):
		"""`!autorolelist` - lists all roles given automatically to new members"""
		with open('serverprefs.json', 'r') as s:
			serverprefs = json.load(s)
		########################################
		svr = str(ctx.message.guild.id)
		role1 = "None"
		role2 = "None"
		role3 = "None"
		role4 = "None"
		role5 = "None"

		if serverprefs[svr]['arole1'] != "":
			role1 = serverprefs[svr]['arole1']
		if serverprefs[svr]['arole2'] != "":
			role2 = serverprefs[svr]['arole2']
		if serverprefs[svr]['arole3'] != "":
			role3 = serverprefs[svr]['arole3']
		if serverprefs[svr]['arole4'] != "":
			role4 = serverprefs[svr]['arole4']
		if serverprefs[svr]['arole5'] != "":
			role5 = serverprefs[svr]['arole5']
		embed = discord.Embed(
			title = "List of Automatically Assigned Roles",
			description = "Role 1: `" + role1 + "`\nRole 2: `" + role2 + "`\nRole 3: `" + role3 + "`\nRole 4: `" + role4 + "`\nRole 5: `" + role5 + "`",
			colour = discord.Colour.blue()
			)
		await ctx.message.channel.send(embed=embed)


		########################################
		with open('serverprefs.json', 'w') as s:
			json.dump(serverprefs, s)



	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def prefix(self, ctx, pfx):
		"""`!prefix PREFIX` - sets prefix - requires admin"""
		with open('serverprefs.json', 'r') as s:
			serverprefs = json.load(s)
		########################################
		sid = ctx.message.guild.id
		channel = ctx.message.channel
		await channel.send("Prefix has been changed to `" + str(pfx) + "`")
		serverprefs[str(sid)]['prefix'] = str(pfx)
		########################################
		with open('serverprefs.json', 'w') as s:
			json.dump(serverprefs, s)
	
	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def prefix(self, ctx, pfx):
		"""`!prefix PREFIX` - sets prefix - requires admin"""
		with open('serverprefs.json', 'r') as s:
			serverprefs = json.load(s)
		########################################
		sid = ctx.message.guild.id
		channel = ctx.message.channel
		await channel.send("Prefix has been changed to `" + str(pfx) + "`")
		serverprefs[str(sid)]['prefix'] = str(pfx)
		########################################
		with open('serverprefs.json', 'w') as s:
			json.dump(serverprefs, s)
			
def setup(bot):
	bot.add_cog(Settings(bot))
	
	
	