from discord.ext import commands
import json
import leveling
import discord

class Points(commands.Cog):
	"""xp"""
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def xp(self, ctx, member: discord.Member = ""):
		"""Gets level and amount of XP"""
		if member == "":
			user = ctx.message.author
		else:
			user = member
		xp = await leveling.get_xp(self.bot, user)
		lvl = await leveling.get_level(self.bot, user)
		nlvl = int(lvl) + 1
		nextxp = await leveling.get_level_xp(int(lvl) + 1)
		rank = await leveling.get_rank(self.bot, user)
		await leveling.makeXpCard(ctx.message, user, int(xp), int(lvl), nlvl, int(nextxp), int(rank))
def setup(bot):
	bot.add_cog(Points(bot))
