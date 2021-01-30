##############
### IMPORT ###
##############

### PACKAGES
import discord
from discord.ext import commands
import json
import os
### FILES
import leveling
import prefs
import meme


######################
### INITIALIZATION ###
######################
async def get_prefix(bot, message):
	await prefs.checkKeys(message.author.guild)
	########################################
	return await prefs.getPfx(message.guild)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
	print("Bot is ready")
	await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!help"))


### COGS ###
@bot.command()
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}')
@bot.command()
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

### sends setup message on join
@bot.event
async def on_guild_join(guild):
	def check(event):
		return event.target.id == bot.user.id
	bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).find(check)
	await bot_entry.user.send("Hello! Thanks for inviting me to " + guild.name + "! Please setup all settings with !help Settings. Please remember that in order to kick/mute etc, my role must be above everyone else's.")

	with open('serverprefs.json', 'r') as s:
		serverprefs = json.load(s)
	########################################
	await prefs.addServerIfNeeded(serverprefs, guild)
	########################################
	with open('serverprefs.json', 'w') as s:
		json.dump(serverprefs, s)

### on join
@bot.event
async def on_member_join(member):
	with open('serverprefs.json', 'r') as s:
			serverprefs = json.load(s)
	########################################
	### AUTOROLE
	await prefs.checkKeys(member.guild)
	sjs = serverprefs[str(member.guild.id)]

	if sjs['arole1'] != '':
		role = discord.utils.get(member.guild.roles, name=str(sjs['arole1']))
		await member.add_roles(role)
	if sjs['arole2'] != '':
		role = discord.utils.get(member.guild.roles, name=str(sjs['arole2']))
		await member.add_roles(role)
	if sjs['arole3'] != '':
		role = discord.utils.get(member.guild.roles, name=str(sjs['arole3']))
		await member.add_roles(role)
	if sjs['arole4'] != '':
		role = discord.utils.get(member.guild.roles, name=str(sjs['arole4']))
		await member.add_roles(role)
	if sjs['arole5'] != '':
		role = discord.utils.get(member.guild.roles, name=str(sjs['arole5']))
		await member.add_roles(role)

	### WELCOME MESSAGE
	cid = serverprefs[str(member.guild.id)]['wmsg']
	channel = discord.utils.get(member.guild.channels, id=cid) 
	await channel.send("Welcome to " + str(member.guild.name) + ", " + member.mention + "!")
	########################################
	with open('serverprefs.json', 'w') as s:
		json.dump(serverprefs, s)



######################
### LEVELING #########
######################
	with open('users.json', 'r') as f:
		users = json.load(f)
	await leveling.createUserIfNeeded(users, member)
	await leveling.updateRanks(users, member)
	with open('users.json', 'w') as f:
		json.dump(users, f)


@bot.event
async def on_message(message):
	if message.author.id == 745135808159285358 or message.author.id == 762732820304232478:
		pass
	else:
		with open('users.json', 'r') as f:
			users = json.load(f)
		await prefs.checkKeys(message.author.guild)
		await leveling.createUserIfNeeded(users, message.author)
		await leveling.addXpCheckLevel(users, message.author, message.channel)
		await leveling.updateRanks(users, message.author)
		with open('users.json', 'w') as f:
			json.dump(users, f)
		await bot.process_commands(message)
	await meme.check(message)
######## COMMANDS ###################################

### on command error
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send(ctx.message.author.mention + ":  " + str(error))
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(ctx.message.author.mention + ":  this is not a command!")

### RUN
bot.run('NzQ1MTM1ODA4MTU5Mjg1MzU4.XztXzA.gbnNfceDBeXf6v5KnXZADXiexDo')

# TEST: NzYyNzMyODIwMzA0MjMyNDc4.X3tcSw.NMLNwb9Mn9pavgLl9bS2RpDKk_g

# NORMAL: NzQ1MTM1ODA4MTU5Mjg1MzU4.XztXzA.gbnNfceDBeXf6v5KnXZADXiexDo