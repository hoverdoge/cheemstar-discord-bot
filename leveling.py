import discord
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import cmask
from discord.utils import get
import math
import funcs


async def createUserIfNeeded(bot, user):
    """Takes bot and user as input. Creates a user entry if needed"""
    sid = str(user.guild.id)
    usid = str(user.id)
    uid = sid + usid
    userObj = await bot.pg_con.fetch("SELECT * FROM users WHERE uniqueid = $1", uid)

    if not userObj:
        await bot.pg_con.execute("INSERT INTO users (level, xp, uniqueid, serverid, userID, rank) VALUES (0, 1, $1, $2, $3, 0)", uid, sid, usid)


async def addXpCheckLevelRanks(bot, user, channel="", xpToAdd = 1):
    """Adds XP and checks levels and ranks. Takes bot, user, channel, and xpToAdd as input."""
    sid = str(user.guild.id)
    uid = str(user.guild.id) + str(user.id)
    userObj = await bot.pg_con.fetchrow("SELECT * FROM users WHERE uniqueID = $1", uid)
    pastLevel = int(userObj['level'])
    await bot.pg_con.execute("UPDATE users SET xp = $1 WHERE uniqueID = $2", userObj['xp'] + xpToAdd, uid)

    newLevel = int(userObj['xp'] ** 1 / 20)
    ### if leveled up
    if pastLevel < newLevel:
        pfp = user.avatar_url
        embed = discord.Embed(
            title=str(user) + " has leveled up!",
            description=user.mention + "has leveled up to level " + str(newLevel),
            colour=discord.Colour.red()
        )
        embed.set_thumbnail(url=(pfp))
        await channel.send(embed=embed)
        await bot.pg_con.execute("UPDATE users SET level = $1 WHERE uniqueID = $2", newLevel, uid)
    ### updates ranks
    usersInServer = await bot.pg_con.fetch("SELECT * FROM users WHERE serverID = $1", sid)
    uisDict = [dict(row) for row in usersInServer]
    await updateRanks(bot, uisDict)


async def get_xp(bot, user):
    """Takes bot and user as parameters. Returns a string with XP value."""
    uid = str(user.guild.id) + str(user.id)
    users = await bot.pg_con.fetchrow("SELECT * FROM users WHERE uniqueID = $1", uid)
    return str(users['xp'])


async def get_level(bot, user):
    """Takes bot and user as parameters. Returns a string with level value."""
    uid = str(user.guild.id) + str(user.id)
    users = await bot.pg_con.fetchrow("SELECT * FROM users WHERE uniqueID = $1", uid)
    return str(users['level'])


async def get_level_xp(level):
    """Takes a level as input. Returns a string with that level's xp requirement."""
    xp = level * 20
    return str(xp)


async def get_rank(bot, user):
    """Takes bot and user as parameters. Returns a string with rank value."""
    uid = str(user.guild.id) + str(user.id)
    users = await bot.pg_con.fetchrow("SELECT * FROM users WHERE uniqueID = $1", uid)
    return str(users['rank'])


async def makeXpCard(message, user, xp, lvl, nlvl, nxp, rank):
    ### setting colors
    primaryC = (255, 255, 255)
    dimC = (128, 128, 128)
    highlightC = (20, 192, 255)
    backgroundC = (30, 30, 30)
    fadedC = (80, 80, 80)

    ### seting up background and font 10, 470, 80
    background = Image.open('images/background.png')
    fnt = ImageFont.truetype('fonts/Arial.ttf', 18)
    sfnt = ImageFont.truetype('fonts/Arial.ttf', 12)
    W = 470
    H = 80

    ####################
    ### RANK DISPLAY ###
    ####################

    ### rank circle
    if rank == 1:
        filename = 'images/goldc.png'
    elif rank == 2:
        filename = 'images/silverc.png'
    elif rank == 3:
        filename = 'images/copperc.png'
    else:
        filename = 'images/dimc.png'
        ### gets rank circle
    arr = await cmask.getRankC(filename)
    newRankC = arr[0]
    rankThumb = arr[1]
    ### pastes rank circle
    newRankC = newRankC.resize((40, 40))
    rankThumb = rankThumb.resize((40, 40))
    background.paste(newRankC, (10, 20), rankThumb)
    ### rank number
    rankN = ImageDraw.Draw(background)
    # centers text
    w, h = fnt.getsize(str(rank))
    # sets text
    rankN.text((25, (H - h) / 2), str(rank), fill=(255, 255, 255), font=fnt)

    ###################
    ### PFP DISPLAY ###
    ###################

    ### gets pfp

    arr = await cmask.getPfp(user)

    newpfp = arr[0]
    pfp_thumb = arr[1]

    ### pastes pfp
    newpfp = newpfp.resize((60, 60))
    pfp_thumb = pfp_thumb.resize((60, 60))
    background.paste(newpfp, (55, 10), pfp_thumb)

    #####################
    ### UNAME DISPLAY ###
    #####################

    ### username

    username = ImageDraw.Draw(background)
    # centers text
    author = str(user)
    index = 0
    i = 0
    for n in author:
        if n == "#":
            index = i
        i += 1

    author = author[:index]
    w, h = fnt.getsize(author)
    username.text((120, (H - h) / 2), author, fill=primaryC, font=fnt)

    ##################
    ### XP DISPLAY ###
    ##################
    xp = funcs.abbrevNum(int(xp))
    xpDraw = ImageDraw.Draw(background)

        # centers text
    w, h = fnt.getsize(str(xp))
    # sets text
    xpDraw.text((419, (H - h) / 2), str(xp), fill=primaryC, font=fnt)

    ##############
    ### XP BAR ###
    ##############
    # barbackground = ImageDraw.Draw(background)
    # barbackground.rectangle((20, 20, 60, 60), fill = 'gold')

    ###################
    ### LVL DISPLAY ###
    ###################
    lvl = funcs.abbrevNum(lvl)

    lvlDraw = ImageDraw.Draw(background)
    # centers text
    w, h = fnt.getsize(str(lvl))
    # sets text
    lvlDraw.text((345, (H - h) / 2), str(lvl), fill=primaryC, font=fnt)

    #################
    ### ROLE DISP ###
    #################
    length = len(user.roles)
    rolename = user.roles[length - 1]
    role = get(user.guild.roles, name=str(rolename))
    rolecolor = role.color

    rDraw = ImageDraw.Draw(background)
    # centers text
    w, h = sfnt.getsize(str(rolename))
    rolecolor = ImageColor.getcolor(str(rolecolor), "RGB")
    # sets text
    rDraw.text((120, ((H - h) / 2) + 15), str(rolename), fill=rolecolor, font=sfnt)

    ### saves sends finished banner and deletes files
    background.save('banner.png')
    await message.channel.send(file=discord.File('banner.png'))
    os.remove('banner.png')
    os.remove('avatar.jpg')
    os.remove('newavatar.png')
    os.remove('newRankC.png')
    os.remove('dimC.png')


async def updateRanks(bot, usersInServerSql):
    usersInServer = {}
    i = 0
    while i < len(usersInServerSql):
        uid = usersInServerSql[i]['uniqueid']
        usersInServer[uid] = usersInServerSql[i]['xp']
        i += 1
    ### sorts all users in server
    usersInServer = dict(sorted(usersInServer.items(), key=lambda x: x[1], reverse=True))
    listUsersInServer = list(usersInServer.keys())
    ### assigns rank
    n = 1
    for uid in listUsersInServer:
        await bot.pg_con.execute("UPDATE users SET rank = $1 WHERE uniqueID = $2", n, uid)
        n += 1
