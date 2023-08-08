import discord
from typing import List
from discord.ext import commands
import os
import main
from nation import Nation
from asset import Asset

# Non Bot Stuff
nation_list: list[Nation] = []
asset_list: list[Asset] = []

# Bot Stuff
bot_intentions = discord.Intents.default() # Intents objects allowing a discord bot to do certain things.
bot_intentions.message_content = True

TOKEN = os.getenv('TOKEN')

# A Bot is a client subclass that allows for fun commands and automatically sets up a command tree for you.
bot = commands.Bot(command_prefix="!rpc ",intents=bot_intentions)
status_channel = None

@bot.command() # This decorator executes below command for the bot when it is called with the bot's prefix and command's name
async def test(context:commands.Context,input_text):
    author = context.message.author
    channel = context.message.channel
    print(author)
    print(channel)
    if channel.name != "bot-testing":
        pass
    else:
        await context.channel.send("Hello")

@bot.command()
async def nationlookup(context:commands.Context,input_text):
    """Gives data on all nation entities in the game"""
    channel = context.message.channel
    author_roles = context.message.author.roles
    for role in author_roles:
        if role.name == ">Administrator":
            for nation in nation_list:
                await channel.send(nation.display())

@bot.event
async def on_ready():
    status_channel = bot.get_channel(1138473460868317254)
    main.load_assets(asset_list)
    await status_channel.send("Asset Loading Complete")
    main.load_nations(nation_list,asset_list)
    await status_channel.send("Nation Loading Complete")

bot.run(TOKEN)

