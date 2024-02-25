import discord
import os
import asyncio
import main
import time
from typing import List
from discord import app_commands
from discord.ext import commands

from nation import Nation
from asset import Asset
import assethandler

TOKEN = os.getenv("TOKEN")

# Non Bot Stuff
nation_list: list[Nation] = []
asset_list: list[Asset] = []
assetStore = assethandler.AssetStore()

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

    # nationinfo
@bot.command()
async def nationinfo(context:commands.Context):
    """Gives data on one nation entities in the game"""
    channel = context.message.channel
    author_roles = context.message.author.roles
    for nation in nation_list:
        if nation.player_name == str(context.message.author.id):
            await channel.send(nation.display())

    # nationeconomy
@bot.command()
async def nationeconomy(context:commands.Context):
    """Gives economic report on nation"""
    channel = context.message.channel
    for nation in nation_list:
        if nation.player_name == str(context.message.author.id):
            await channel.send(nation.economy_prediction())

    # nationlookupall
@bot.command()
async def nationlookupall(context:commands.Context):
    """Gives data on all nation entities in the game"""
    channel = context.message.channel
    author_roles = context.message.author.roles
    for role in author_roles:
        if role.name == ">Administrator":
            for nation in nation_list:
                await channel.send(nation.display())


    #savenations
@bot.command()
async def savenations(context:commands.Context):
    channel = context.message.channel
    author_roles = context.message.author.roles
    for role in author_roles:
        if role.name == ">Administrator":
            main.save_assets(asset_list)
            main.save_nations(nation_list)

    #managenation
@bot.command()
async def managenation(context:commands.Context):
    """ A command that allows the user to access nation assets or build new ones"""

    try:
        channel = context.message.channel
        author = context.author
        cur_nation = None
        
        def check(m:discord.Message)->bool: # Check used to validate input
            return(m.author == author)


        for nation in nation_list: # Find the player nation
            if nation.player_name == str(context.author.id):
                cur_nation = nation
        if type(cur_nation) == Nation: # Continue
            await channel.send(
f'''
{cur_nation.name} Management - Please choose
1. Acquire new assets
2. Manage assets
3. Cancel
''')
            
            # Decide which direction to proceed
            menu_choice = int((await bot.wait_for('message',check=check)).content)
            selected_asset_text = ""
            
            if menu_choice == 1: # Buy Asset

                await channel.send("Which type of asset would you like to view? wealth/political/force")
                
                type_choice = (await bot.wait_for('message',check=check)).content # Get type 

                if type_choice == "wealth": # Wealth assets
                    await channel.send("__Select which asset to build:__ (Write the name)")
                    text = ""
                    for asset in assetStore.wealth_assets:
                        text+=f"- {asset}\n"

                    await channel.send(text)
                    
                    selected_asset_text = ((await bot.wait_for('message',check=check)).content.title())

                    
                elif type_choice == "political":
                    pass
                
                elif type_choice == "force":
                    pass 
                
                
                try: # Try creating the asset
                    selected_asset = assetStore.wealth_assets[selected_asset_text]
                    created_asset:Asset = selected_asset()
                    if created_asset.cost_calculation(cur_nation): # Check if can add to nation
                        created_asset.uid = assetStore.idpointer
                        assetStore.idpointer+=1
                        created_asset.building_purchase(cur_nation)
                        asset_list.append(created_asset)
                    else:
                        await channel.send(f"Not enough resources to create {created_asset.name}")

                        
                    
                except:
                    await channel.send("Unregistered input")

            elif menu_choice == 2:
                pass # print assets and allow user to pick one
            elif menu_choice == 3:
                await channel.send("Cancelling management")
            else:
                await channel.send("Unrecognised command, exiting management")
            
        else: # Exit code
            await channel.send("Nation not found")
    except asyncio.TimeoutError:
        await channel.send("Bot Timed Out")
    
    # shutdown
@bot.command()
@commands.is_owner()
async def shutdown(context:commands.Context):
    print(f"shutting down at {time.ctime(time.time())}")
    main.save_assets(asset_list)
    print("Assets Saved")
    main.save_nations(nation_list)
    print("Nations Saved")
    await bot.close()
    await exit(0)

    # nationsignup
@bot.command()
async def nationsignup(context: commands.Context):
    """Returns a prompt allowing the user to fill in Nation details then processes it."""
    original_channel = context.channel
    DM_target = context.author
    owner_id = DM_target.id
    await DM_target.send("Please input full nation name: ")
    
    def check(m:discord.Message)->bool: # Will be used to see if replies to the bot are given by the command user & in the DMs.
        return(m.author==DM_target and m.channel==DM_target.dm_channel) 
    
    try: 
        # Nation Name
        nation_name = await bot.wait_for('message',check=check)

        # Nation Continent
        await DM_target.send("Pick starting continent - Options include: Asia, North America, South America, Africa, Antarctica, Europe, Oceania")
        starting_region = await bot.wait_for('message',check=check)


        # Urban Pop
        await DM_target.send("Pick starting Urban Population: Please write whole numbers, with no punctuation e.g 10000000 for 10 million")
        urban_population = await bot.wait_for('message',check=check)
    
        # Rural Pop
        await DM_target.send("Pick starting Rural Population: Please write whole numbers, with no punctuation e.g 10000000 for 10 million")
        rural_population = await bot.wait_for('message',check=check)

    
        points_left = 5
        await DM_target.send(f"You have 5 starting points to distribute between your nation's aspects. Consult the spreadsheet to find out what points get you")
        await DM_target.send(f"You have {points_left} points left. How many to distribute to wealth?")
        wealth_points = int((await (bot.wait_for('message',check=check))).content) # Need to convert discord.Message to int
        points_left-=wealth_points

    
        await DM_target.send(f"You have {points_left} points left. How many to distribute to political?")
        political_points = int((await (bot.wait_for('message',check=check))).content)
        points_left -= political_points

        await DM_target.send(f"Allocating {points_left} to force")
        force_points = points_left
        new_nation = Nation()
        new_nation.import_data_on_create(nation_name.content,int(urban_population.content),int(rural_population.content),wealth_points,political_points,force_points,owner_id,starting_region.content)
        print(f"succesfully created {nation_name.content}")
                    
        nation_list.append(new_nation)    
        main.save_nations(nation_list)
        await DM_target.send(f"Succesfully created {nation_name.content}, enjoy playing :)")
    except asyncio.TimeoutError:
        await DM_target.send("Timeout error. Please try again")


@bot.event
async def on_ready():
    status_channel = bot.get_channel(1138473460868317254)
    main.load_assets(asset_list)
    assetStore.idpointer = len(asset_list)
    await status_channel.send("Asset Loading Complete")
    main.load_nations(nation_list,asset_list)
    await status_channel.send("Nation Loading Complete")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")

#bot.run(TOKEN)

if __name__ == "__main__":
  asyncio.run(runner(bot))