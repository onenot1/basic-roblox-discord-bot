import asyncio
import discord
import roblox
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
roClient = roblox.Client()

prefix = "!"

async def display_help(message):
    total_message = ""
    for command in command_descriptions:
        total_message += command + "\n"
    await message.channel.send("```\n" + total_message + "\n```")

async def channels(message):
    categoryChannel = ""
    textChannel = ""
    voiceChannel = ""
    for channel in client.get_all_channels():
        if type(channel) == discord.channel.CategoryChannel:
            categoryChannel += "    - " + str(channel) + "\n"
        elif type(channel) == discord.channel.TextChannel:
            textChannel += "    - " + str(channel) + "\n"
        else:
            voiceChannel += "    - " + str(channel) + "\n"
    await message.channel.send("```\n" + "Here are all the channels:\n\n" + "Category Channels:\n" + categoryChannel + "\n" + "Text Channels:\n" + textChannel + "\n" + "Voice Channels:\n" + voiceChannel + "\n```")

async def get_player_follower_count(message):
    user = await roClient.get_user_by_username(str(str.split(message.content)[1]))
    await message.channel.send(
        "The player has " + str(await user.get_follower_count()) + " users following them."
    )

async def get_followers(message):
    user = await roClient.get_user_by_username(str(str.split(message.content)[1]))
    await message.channel.send(
        user.get_followers()
    )

commands = {
    "help": display_help,
    "channels": channels,
    "playerfollowers": get_player_follower_count,
    "getfollowers": get_followers
}

command_descriptions = {
    "!help - Displays all commands",
    "!channels - Displays all channels in a server",
    "!playerfollowing [user] - Displays amount of people following user",
    "!getfollowers [user] - Displays the followers of said user"
}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if (message.author != client.user):
        for command in commands:
            if (message.content.startswith(prefix + command)):
                await commands.get(command)(message)

@client.event
async def on_message_delete(message):
    if (message.author != client.user):
        await message.channel.send(str(message.author) + " deleted a message saying: \n" + str(message.content))



client.run('put your token here')