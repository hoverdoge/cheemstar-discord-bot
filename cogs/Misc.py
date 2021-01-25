from discord.ext import commands
import discord
import random

class Misc(commands.Cog):
	"""help, coinflip, poll, tts"""
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	@commands.has_permissions(add_reactions=True,embed_links=True)
	async def help(self,ctx,*cog):
		"""Gets all commands"""
		try:
			if not cog:
				halp=discord.Embed(title='Command Categories',
								description='Use `!help *category*` to find out more about them!\n')
				cogs_desc = ''
				for x in self.bot.cogs:
					cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
				halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
				cmds_desc = ''
				for y in self.bot.walk_commands():
					if not y.cog_name and not y.hidden:
						cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
				await ctx.message.add_reaction(emoji='✉')
				await ctx.message.author.send('',embed=halp)
			else:
				if len(cog) > 1:
					halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
					await ctx.message.author.send('',embed=halp)
				else:
					found = False
					for x in self.bot.cogs:
						for y in cog:
							if x == y:
								halp=discord.Embed(title=cog[0]+' Command Listing')
								for c in self.bot.get_cog(y).get_commands():
									if not c.hidden:
										halp.add_field(name=c.name,value=c.help,inline=False)
								found = True
					if not found:
						halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
					else:
						await ctx.message.add_reaction(emoji='✉')
					await ctx.message.author.send('',embed=halp)
		except:
			pass

	###################
	@commands.command()
	async def coinflip(self, ctx):
		"""`!coinflip` - Returns heads or tails randomly"""
		await ctx.message.add_reaction(emoji='🪙')
		num = random.randint(0, 1)
		if num == 0:
			await ctx.message.channel.send("Heads")
		else:
			await ctx.message.channel.send("Tails")

	###################
	@commands.command()
	async def poll(self, ctx, *, msg):
		"""`!poll *title*,*description*,*emoji*,*emoji*...` - makes a poll. 2-5 emojis required."""
		prms = msg.split(",")

		pfp = ctx.message.author.avatar_url
		embed = discord.Embed(
            title=prms[0],
            description=prms[1],
            colour=discord.Colour.blue()
        )
        # embed.set_thumbnail(url=(pfp))
		embed.set_footer(text="\n \n Poll started by " + str(ctx.message.author), icon_url=pfp)
		embedm = await ctx.message.channel.send(embed=embed)

		if len(prms) >= 4:
			await embedm.add_reaction(prms[2].strip())
			await embedm.add_reaction(prms[3].strip())
			if len(prms) >= 5:
				await embedm.add_reaction(prms[4].strip())
				if len(prms) >= 6:
					await embedm.add_reaction(prms[5].strip())
					if len(prms) >= 7:
						await embedm.add_reaction(prms[6].strip())	

	@commands.command()
	@commands.has_permissions(send_tts_messages=True)
	async def tts(self, ctx):
		"""`!tts *message*` - splits up message to bypass tts limit - requires tts permission."""
		msg = ctx.message.content[5:]
		ttsArr = [msg[i:i+200] for i in range(0, len(msg), 200)]
		length = len(ttsArr)
		i = 0
		while i < length:
			await ctx.send(ttsArr[i], tts=True)
			i += 1

def setup(bot):
	bot.add_cog(Misc(bot))