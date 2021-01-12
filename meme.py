import discord

async def check(message):
	msg = message.content
	chns = message.channel.send
	if msg == "perhaps":
		await chns(file=discord.File('memes/perhaps.jpeg'))
	if msg == "mono":
		await chns(file=discord.File('memes/no.jpg'))