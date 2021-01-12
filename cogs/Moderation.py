import time
import discord
from discord.ext import commands

class Moderation(commands.Cog):
	"""clear, ban, kick, mute, unmute, warn"""
	def __init__(self, bot):
		self.bot = bot

	### CLEAR
	@commands.command()
	@commands.has_permissions(manage_messages=True) 
	async def clear(self, ctx):
		"""`!clear x` - clears x amount of messages - requires permission to manage messages"""
		m = int(ctx.message.content.replace('!clear ', ''))
		if (m <= 1000):
			await ctx.message.channel.purge(limit = m + 1)
			embed = discord.Embed(
				title = "**Deleted " + str(m) + " messages! ** (" + str(ctx.message.author) + ")",
				colour = discord.Colour.red()
				)
			msg = await ctx.message.channel.send(embed=embed) 
			time.sleep(3)
			await msg.delete()
		else:
			await ctx.message.channel.send("Cannot clear more than 1000 messages at once")

	### BAN 
	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		"""`!ban @user` - bans user - requires permission to ban members"""
		await member.ban(reason=reason)
		await ctx.send(f'User {member} has been banned')
	### KICK
	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member : discord.Member, *, reason=None):
		"""`!kick @user` - kicks user - requires permission to kick members"""
		await member.kick(reason=reason)
		await ctx.send(f'User {member} has been kicked')

	### MUTE
	@commands.command()
	@commands.has_permissions(mute_members=True)
	async def mute(self, ctx, member : discord.Member):
		"""`!mute @user` - mutes user - requires permission to mute members"""
		await member.edit(mute = True)
	### UNMUTE
	@commands.command()
	@commands.has_permissions(mute_members=True)
	async def unmute(self, ctx, member : discord.Member):
		"""`!unmute @user` - unmutes user - requires permission to mute members"""
		await member.edit(mute = False)

	### WARN
	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def warn(self, ctx, member : discord.Member, *, reason):
		"""`!warn @user reason` - warns user - requires permission to kick members"""
		pfp = member.avatar_url
		embed = discord.Embed(
			title = str(member) + " has been warned!",
			description = member.mention + "\n**Reason:** " + reason,
			colour = discord.Colour.red()
			)
		embed.set_thumbnail(url=(pfp))
		await ctx.message.channel.send(embed=embed)

	### FREEZE
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def freeze(self, ctx):
		"""`!freeze` - puts slowmode on a channel for an hour - requires manage messages"""
		await ctx.channel.edit(slowmode_delay = 3600)
		await ctx.send("Channel has been frozen")

	### UNFREEZE
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def unfreeze(self, ctx):
		"""`!unfreeze` - removes slowmode on a channel - requires manage messages"""
		await ctx.channel.edit(slowmode_delay = 0)
		await ctx.send("Channel has been unfrozen")
 
def setup(bot):
	bot.add_cog(Moderation(bot))