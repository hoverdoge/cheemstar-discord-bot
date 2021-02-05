import discord
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import cmask
from discord.utils import get
import json
import math
import funcs

async def createUserIfNeeded(users, user):
    uid = str(user.guild.id) + str(user.id)
    if uid not in users:
        users[uid] = {}
        users[uid]['xp'] = 0
        users[uid]['level'] = 0
        users[uid]['rank'] = 0
        users[uid]['server'] = user.guild.id
        users[uid]['user'] = user.id


async def addXpCheckLevel(users, user, channel, xpToAdd = 1):
    uid = str(user.guild.id) + str(user.id)
    pastLevel = int(users[uid]['level'])
    users[uid]['xp'] += xpToAdd
    newLevel = int(users[uid]['xp'] ** 1 / 20)
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
        users[uid]['level'] = newLevel

async def get_xp(users, user):
    uid = str(user.guild.id) + str(user.id)
    return str(users[uid]['xp'])


async def get_level(users, user):
    uid = str(user.guild.id) + str(user.id)
    return str(users[uid]["level"])


async def get_level_xp(level):
    xp = level * 20
    return str(xp)


async def get_rank(users, user):
    uid = str(user.guild.id) + str(user.id)
    return str(users[uid]['rank'])


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


async def updateRanks(users, user):
    usersInServer = {}
    for i in users:
        if users[i]['server'] == user.guild.id:
            usersInServer[i] = users[i]['xp']
    ### sorts all users in server
    usersInServer = dict(sorted(usersInServer.items(), key=lambda x: x[1], reverse=True))
    listUsersInServer = list(usersInServer.keys())
    ### assigns rank
    for uid in users:
        n = 1
        for user in listUsersInServer:
            if uid == user:
                users[uid]['rank'] = n
            n += 1
