from discord.ext import commands
import json
import leveling
import discord

class Points(commands.Cog):
	"""xp"""
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def xp(self, ctx, member : discord.Member = ""):
		"""Gets level and amount of XP"""
		with open('users.json', 'r') as f:
			users = json.load(f)
		if member == "":
			user = ctx.message.author
		else:
			user = member

		xp = await leveling.get_xp(users, user)
		lvl = await leveling.get_level(users, user)
		nlvl = int(lvl) + 1
		nextxp = await leveling.get_level_xp(int(lvl) + 1)
		rank = await leveling.get_rank(users, user)
		await leveling.makeXpCard(ctx.message, user, int(xp), int(lvl), nlvl, int(nextxp), int(rank))
def setup(bot):
	bot.add_cog(Points(bot))
