from discord.ext import commands
import json
import leveling
import discord

class Development(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def givexp(self, ctx, member: discord.Member, xptg):
        with open('users.json', 'r') as f:
            users = json.load(f)
        #####################################
        await ctx.send("`" + str(member) + "`,`+" + str(xptg) + "`")
        await leveling.createUserIfNeeded(users, member)
        await leveling.addXpCheckLevel(users, member, ctx.message.channel, int(xptg))
        await leveling.updateRanks(users, member)
        #####################################
        with open('users.json', 'w') as f:
            json.dump(users, f)

    @commands.command()
    @commands.is_owner()
    async def nullxp(self, ctx, member: discord.Member):
        with open('users.json', 'r') as f:
            users = json.load(f)
        #####################################
        xptt = await leveling.get_xp(users, member)
        await ctx.send("taken")
        await leveling.createUserIfNeeded(users, member)
        users[str(member.guild.id) + str(member.id)]['xp'] = 1
        users[str(member.guild.id) + str(member.id)]['level'] = 0
        await leveling.updateRanks(users, member)
        #####################################
        with open('users.json', 'w') as f:
            json.dump(users, f)
def setup(bot):
    bot.add_cog(Development(bot))
