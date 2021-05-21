from discord.ext import commands
import json
import discord
from discord.utils import get

class Settings(commands.Cog):
	"""welcomechannel, autorole, autorolelist, prefix"""
	def __init__(self, bot):
		self.bot = bot

	### WELCOME CHANNEL ###
	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def welcomechannel(self, ctx):
		"""`!welcomechannel` - channel welcome messages are sent in - requires admin"""
		sid = str(ctx.message.guild.id)
		channel = ctx.message.channel
		await self.bot.pg_con.execute("UPDATE serverprefs SET wchnl = $1 WHERE serverid = $2", str(channel.id), sid)
		await channel.send("Welcome messages will now be sent to `" + str(channel) + "`")

	### WELCOME CHANNEL ###
	@commands.command()
	@commands.has_permissions(manage_roles=True) 
	async def autorole(self, ctx):
		"""`!autorole ROLE` - gives new members a certain role (up to 5 addable) - requires manage roles"""
		sid = str(ctx.message.guild.id)
		serverprefs = await self.bot.pg_con.fetchrow("SELECT * FROM serverprefs WHERE serverid = $1", sid)
		role = str(ctx.message.content)[10:]

		if not get(ctx.guild.roles, name=role):
			await ctx.message.channel.send("Role `" + role + "` does not exist.")

		else:
			if serverprefs['arole1'] == " ":
				await self.bot.pg_con.execute("UPDATE serverprefs SET arole1 = $1 WHERE serverid = $2", role, sid)
				await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
			elif serverprefs['arole2'] == " ":
				await self.bot.pg_con.execute("UPDATE serverprefs SET arole2 = $1 WHERE serverid = $2", role, sid)
				await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
			elif serverprefs['arole3'] == " ":
				await self.bot.pg_con.execute("UPDATE serverprefs SET arole3 = $1 WHERE serverid = $2", role, sid)
				await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
			elif serverprefs['arole4'] == " ":
				await self.bot.pg_con.execute("UPDATE serverprefs SET arole4 = $1 WHERE serverid = $2", role, sid)
				await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
			elif serverprefs['arole5'] == " ":
				await self.bot.pg_con.execute("UPDATE serverprefs SET arole5 = $1 WHERE serverid = $2", role, sid)
				await ctx.message.channel.send("`" + str(role) + "` will now be added to all members upon joining.")
			else:
				await ctx.message.channel.send("You already have 5 roles. Your autorole list has been cleared.")
				serverprefs['arole1'] = " "
				serverprefs['arole2'] = " "
				serverprefs['arole3'] = " "
				serverprefs['arole4'] = " "
				serverprefs['arole5'] = " "

	@commands.command()
	async def autorolelist(self, ctx):
		"""`!autorolelist` - lists all roles given automatically to new members"""
		svr = str(ctx.message.guild.id)
		serverprefs = await self.bot.pg_con.fetchrow("SELECT * FROM serverprefs WHERE serverid = $1", str(ctx.message.guild.id))
		role1 = "None"
		role2 = "None"
		role3 = "None"
		role4 = "None"
		role5 = "None"

		if serverprefs['arole1'] != " ":
			role1 = serverprefs['arole1']
		if serverprefs['arole2'] != " ":
			role2 = serverprefs['arole2']
		if serverprefs['arole3'] != " ":
			role3 = serverprefs['arole3']
		if serverprefs['arole4'] != " ":
			role4 = serverprefs['arole4']
		if serverprefs['arole5'] != " ":
			role5 = serverprefs['arole5']
		embed = discord.Embed(
			title = "List of Automatically Assigned Roles",
			description = "Role 1: `" + role1 + "`\nRole 2: `" + role2 + "`\nRole 3: `" + role3 + "`\nRole 4: `" + role4 + "`\nRole 5: `" + role5 + "`",
			colour = discord.Colour.blue()
			)
		await ctx.message.channel.send(embed=embed)

	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def prefix(self, ctx, pfx):
		"""`!prefix PREFIX` - sets prefix - requires admin"""
		sid = ctx.message.guild.id
		channel = ctx.message.channel
		await self.bot.pg_con.execute("UPDATE serverprefs SET prefix = $1 WHERE serverid = $2", str(pfx), str(sid))
		await channel.send("Prefix has been changed to `" + str(pfx) + "`")
def setup(bot):
	bot.add_cog(Settings(bot))
	
	
	