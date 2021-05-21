from discord.ext import commands
import json
import leveling
import discord

class Development(commands.Cog):
    """don't even try, you can't use any of these"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def givexp(self, ctx, member: discord.Member, xptg):
        await ctx.send("`" + str(member) + "`,`+" + str(xptg) + "`")
        await leveling.createUserIfNeeded(self.bot, member)
        uid = str(member.guild.id) + str(member.id)
        userObj = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE uniqueid = $1", uid)
        oldXp = userObj['xp']
        await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE uniqueid = $2", xptg + oldXp, uid)
        await leveling.addXpCheckLevelRanks(self.bot, member, ctx.message.channel, 0)

    @commands.command()
    @commands.is_owner()
    async def nullxp(self, ctx, member: discord.Member):
        xptt = await leveling.get_xp(self.bot, member)
        await ctx.send("taken")
        await leveling.createUserIfNeeded(self.bot, member)
        await leveling.addXpCheckLevelRanks(self.bot, member, ctx.message.channel, (-1 * int(xptt)))
def setup(bot):
    bot.add_cog(Development(bot))
