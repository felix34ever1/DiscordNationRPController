import discord
import os
import asyncio
import main
from typing import List
from discord import app_commands
from discord.ext import commands

from nation import Nation
from asset import Asset

TOKEN = os.getenv("TOKEN")

# Non Bot Stuff
nation_list: list[Nation] = []
asset_list: list[Asset] = []

# Bot Stuff
bot_intentions = discord.Intents.default() # Intents objects allowing a discord bot to do certain things.
bot_intentions.message_content = True

# A Bot is a client subclass that allows for fun commands and automatically sets up a command tree for you.
bot = commands.Bot(command_prefix="!rpc ",intents=bot_intentions)
status_channel = None

async def runner(bot):
    await bot.start(os.getenv("TOKEN"))

    # test
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

    # nationlookup
@bot.command()
async def nationlookup(context:commands.Context,input_text):
    """Gives data on all nation entities in the game"""
    channel = context.message.channel
    author_roles = context.message.author.roles
    for role in author_roles:
        if role.name == ">Administrator":
            for nation in nation_list:
                if nation.name == input_text:
                    await channel.send(nation.display())


    # shutdown
@bot.command()
@commands.is_owner()
async def shutdown(context:commands.Context):
    await context.bot.close()
    await exit(0)

    # nationsignup
@bot.command()
async def nationsignup(context: commands.Context):
    """Returns a prompt allowing the user to fill in Nation details then processes it."""
    original_channel = context.channel
    DM_target = context.author
    await DM_target.send("Please input full nation name: ")
    
    def check(m:discord.Message)->bool: # Will be used to see if replies to the bot are given by the command user & in the DMs.
        return(m.author==DM_target and m.channel==DM_target.dm_channel) 
    
    try: # Nation Name
        nation_name = await bot.wait_for('message',check=check)
    except asyncio.TimeoutError:
        await DM_target.send("Timeout error. Please try again")
    else:
        try: # Nation Continent
            await DM_target.send("Pick starting continent - Options include: Asia, North America, South America, Africa, Antarctica, Europe, Oceania")
            starting_region = await bot.wait_for('message',check=check)
        except asyncio.TimeoutError:
            await DM_target.send("Timeout error. Please try again")
        else:
            try: # Urban Pop
                await DM_target.send("Pick starting Urban Population: Please write whole numbers, with no punctuation e.g 10000000 for 10 million")
                urban_population = await bot.wait_for('message',check=check)
            except asyncio.TimeoutError:
                await DM_target.send("Timeout error. Please try again")
            else:
                try: # Rural Pop
                    await DM_target.send("Pick starting Rural Population: Please write whole numbers, with no punctuation e.g 10000000 for 10 million")
                    rural_population = await bot.wait_for('message',check=check)
                except asyncio.TimeoutError:
                    await DM_target.send("Timeout error. Please try again")
                else:
                    try: # Wealth Points
                        points_left = 5
                        await DM_target.send(f"You have 5 starting points to distribute between your nation's aspects. Consult the spreadsheet to find out what points get you")
                        await DM_target.send(f"You have {points_left} points left. How many to distribute to wealth?")
                        wealth_points = int((await (bot.wait_for('message',check=check))).content) # Need to convert discord.Message to int
                        points_left-=wealth_points
                    except asyncio.TimeoutError:
                        await DM_target.send("Timeout error. Please try again")
                    else:
                        try: # Political Points
                            await DM_target.send(f"You have {points_left} points left. How many to distribute to political?")
                            political_points = int((await (bot.wait_for('message',check=check))).content)
                            points_left -= political_points
                        except asyncio.TimeoutError:
                            await DM_target.send("Timeout error. Please try again")
                        else:
                            DM_target.send(f"Allocating {points_left} to force")
                            force_points = points_left
                            new_nation = Nation()
                            new_nation.import_data_on_create(nation_name.content,int(urban_population.content),int(rural_population.content),wealth_points,political_points,force_points)
                            print(f"succesfully created {nation_name.content}")
                            nation_list.append(new_nation)    
                        


@bot.event
async def on_ready():
    status_channel = bot.get_channel(1138473460868317254)
    main.load_assets(asset_list)
    await status_channel.send("Asset Loading Complete")
    main.load_nations(nation_list,asset_list)
    await status_channel.send("Nation Loading Complete")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")

#bot.run(TOKEN)

if __name__ == "__main__":
  asyncio.run(runner(bot))