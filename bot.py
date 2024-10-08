import discord
import os
import asyncio
import main
import time
from typing import List
from discord import app_commands
from discord.ext import commands

from nation import Nation
from asset import Asset,UnitGroup,Unit
from war import War,nextWarID,Front,nextFrontID
import assethandler

TOKEN = os.getenv("TOKEN")

# Non Bot Stuff
nation_list: list[Nation] = []
asset_list: list[Asset] = []
war_list: list[War] = []
front_list: list[Front] = []
assetStore = assethandler.AssetStore(asset_list,nation_list)

# Bot Stuff
bot_intentions = discord.Intents.default() # Intents objects allowing a discord bot to do certain things.
bot_intentions.message_content = True

# A Bot is a client subclass that allows for fun commands and automatically sets up a command tree for you.
bot = commands.Bot(command_prefix="!rpc ",intents=bot_intentions)
bot.allowed_mentions = discord.AllowedMentions(everyone=None,roles=False,users=False)
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
    
@bot.command() # nationinfo
async def nationinfo(context:commands.Context):
    """Gives data on one nation entities in the game"""
    channel = context.message.channel
    author_roles = context.message.author.roles
    for nation in nation_list:
        if nation.player_name == str(context.message.author.id):
            await channel.send(nation.display())

@bot.command() # nationeconomy
async def nationeconomy(context:commands.Context):
    """Gives economic report on nation"""
    channel = context.message.channel
    for nation in nation_list:
        if nation.player_name == str(context.message.author.id):
            await channel.send(nation.economy_prediction())

@bot.command() # nationlookupall
async def nationlookupall(context:commands.Context):
    """Gives data on all nation entities in the game"""
    channel = context.message.channel
    author_roles = context.message.author.roles
    for role in author_roles:
        if role.name == ">Administrator":
            for nation in nation_list:
                await channel.send(nation.display())

@bot.command() # savenations
async def savenations(context:commands.Context):
    channel = context.message.channel
    author_roles = context.message.author.roles
    for role in author_roles:
        if role.name == ">Administrator":
            main.save_assets(asset_list)
            main.save_nations(nation_list)
            main.save_fronts(front_list)
            main.save_wars(war_list)
  
@bot.command() #managenation
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
3. Trade
4. Cancel
''')
            
            nation.economy_prediction()

            # Decide which direction to proceed
            menu_choice = int((await bot.wait_for('message',check=check)).content)
            selected_asset_text = ""
            
            if menu_choice == 1: # Buy Asset

                await channel.send("Which type of asset would you like to purchase? wealth/political/force")
                
                type_choice = (await bot.wait_for('message',check=check)).content # Get type 

                if type_choice == "wealth" or type_choice == "political" or type_choice == "force": # Wealth assets

                    await channel.send(assetStore.preview_assets(type_choice,cur_nation.get_attribute(type_choice)))
                    
                    selected_asset_text = ((await bot.wait_for('message',check=check)).content.title())

                    try:
                        asset_directed = assetStore.get_asset_directed(selected_asset_text,type_choice)
                        
                        if asset_directed == "directed":
                            nation_text = "__Pick Target Nation by number:__\n"
                            for nation in nation_list:
                                nation_text+=f"- {nation_list.index(nation)} - {nation.name}\n"
                            await channel.send(nation_text)
                            input_nation = int((await bot.wait_for("message",check=check)).content)
                            if input_nation < len(nation_list) and input_nation>=0:
                                target_nation = nation_list[input_nation]
                                affirmation_message = assetStore.buy_directed_asset(selected_asset_text,type_choice,cur_nation,target_nation)
                            else:
                                affirmation_message = "Nation you chose is out of bounds"
                        else:
                            affirmation_message = assetStore.buy_asset(selected_asset_text,type_choice,cur_nation)
                        await channel.send(affirmation_message)
                    except:
                        await channel.send("Unregistered Input")
                    
                else:
                    await channel.send("Unregistered Type")


            elif menu_choice == 2:  # Manage Asset - print assets and allow user to pick one
                await channel.send("Which type of asset would you like to view? wealth/political/force")
                type_choice = (await bot.wait_for("message", check=check)).content
                
                text = "Please choose an asset by ID:\nID - Name\n"
                if type_choice == "wealth":
                    for asset in cur_nation.assets_wealth:
                        text+=(f"{asset.uid} - {asset.name}\n")
                elif type_choice == "political":
                    for asset in cur_nation.assets_political:
                        text+=(f"{asset.uid} - {asset.name}\n")
                elif type_choice == "force":
                    for asset in cur_nation.assets_force:
                        text+=(f"{asset.uid} - {asset.name}\n")
                await channel.send(text)

                id_choice = int((await bot.wait_for('message',check=check)).content)

                chosen_asset:Asset = None
                if type_choice == "wealth":
                    for asset in cur_nation.assets_wealth:
                        if asset.uid == id_choice:
                            chosen_asset = asset
                elif type_choice == "political":
                    for asset in cur_nation.assets_political:
                        if asset.uid == id_choice:
                            chosen_asset = asset
                elif type_choice == "force":
                    for asset in cur_nation.assets_force:
                        if asset.uid == id_choice:
                            chosen_asset = asset

                if isinstance(chosen_asset,Asset):
                    if chosen_asset.construction_time==0:
                        if chosen_asset.activated:
                            await channel.send(f"{chosen_asset.name} is working correctly")
                        else:
                            await channel.send(f"{chosen_asset.name} has halted working")
                        # run asset management command
                        await chosen_asset.manage(bot,channel,author)
                    else:
                        await channel.send(f"{chosen_asset.name} is still under construction for {chosen_asset.construction_time} turns")

                    # Instead of deleting asset, go to the asset manage command

                    await channel.send("Delete Asset? yes/no")
                    asset_delete_choice = (await bot.wait_for("message",check=check)).content

                    if asset_delete_choice == "yes":
                        asset_list.remove(chosen_asset)
                        chosen_asset.delete_self()
                        
                        print(f"Deleted asset")
                


            elif menu_choice == 3:
                await channel.send("Cancelling management")
            else:
                await channel.send("Unrecognised command, exiting management")
            
        else: # Exit code
            await channel.send("Nation not found")
    except asyncio.TimeoutError:
        await channel.send("Bot Timed Out") # Shutdown

    # editgroup
@bot.command() #editgroup
async def editgroup(context:commands.Context):
    """ A command that allows the user to access nation unit groups and add units to them"""

    try:
        channel = context.message.channel
        author = context.author
        cur_nation = None
        
        def check(m:discord.Message)->bool: # Check used to validate input
            return(m.author == author)


        for nation in nation_list: # Find the player nation
            if nation.player_name == str(context.author.id):
                cur_nation = nation
        if cur_nation == None:
            raise Exception("No player nation found, please sign up first.")
        if type(cur_nation) == Nation: # Continue
            await channel.send(f"Please select group to manage:\nID -- Name")
            text = ""
            unitgroups:list[UnitGroup] = [] # Used to keep all unit groups together for later checking of where units are.
            for asset in cur_nation.assets_wealth:
                if isinstance(asset,UnitGroup):
                    unitgroups.append(asset)
                    text+=(f"{asset.uid} - {asset.nickname}\n")
            for asset in cur_nation.assets_political:
                if isinstance(asset,UnitGroup):
                    unitgroups.append(asset)
                    text+=(f"{asset.uid} - {asset.nickname}\n")
            for asset in cur_nation.assets_force:
                if isinstance(asset,UnitGroup):
                    unitgroups.append(asset)
                    text+=(f"{asset.uid} - {asset.nickname}\n")
            await channel.send(text)
            choice = int((await bot.wait_for("message",check=check)).content)
            # TODO Get the unit group,
            selected_unitgroup = None
            for asset in cur_nation.assets_wealth:
                if isinstance(asset,UnitGroup) and asset.uid == choice:
                    selected_unitgroup = asset
            for asset in cur_nation.assets_political:
                if isinstance(asset,UnitGroup) and asset.uid == choice:
                    selected_unitgroup = asset
            for asset in cur_nation.assets_force:
                if isinstance(asset,UnitGroup) and asset.uid == choice:
                    selected_unitgroup = asset
            if selected_unitgroup != None:
                await channel.send(f"Selected {selected_unitgroup.nickname}:")
                ended = False
                while not ended: # Loop ability to do stuff until player wants to break loop
                    await channel.send(
                #  then present user with valid units that can go in battlegroup (showing which are already assigned elsewhere) 
                # and let user put units in battlegroup until they type end or close
f"""1. Remove current units
2. Add new units
3. Stop
""")            
                    choice = int((await bot.wait_for("message",check=check)).content)
                    if choice == 1: # Remove units
                        await channel.send("Choose unit ID to remove from unitgroup.")
                        text = ""
                        for unit in selected_unitgroup.unit_list:
                            text+=f"{unit.uid} -- Nickname:{unit.nickname}\n"
                        await channel.send(text)
                        unitidchoice = int((await bot.wait_for("message",check=check)).content)
                        for unit in selected_unitgroup.unit_list:
                            if unit.uid == unitidchoice:
                                # Remove unit from battlegroup, and remove its locked attack unit.
                                selected_unitgroup.unit_id_list.remove(unit.uid)
                                selected_unitgroup.unit_list.remove(unit)
                                if unit.locked_unit != None: # Remove also 
                                    unit.locked_unit.locked_unit=None
                                    unit.locked_unit.locked_unit_id=None
                                unit.locked_unit = None
                                unit.locked_unit_id = None
                    
                    elif choice == 2: # Add units
                        # Go through units adding them to text
                        units:list[Unit] = []
                        text = ""
                        for asset in cur_nation.assets_wealth:
                            if isinstance(asset,Unit):
                                #Verify that unit can be in the battlespaces of the unitgroup
                                for possible_battlespace in asset.possible_battlespaces:
                                    if possible_battlespace in selected_unitgroup.battlespaces:
                                        units.append(asset)
                                        break
                        for asset in cur_nation.assets_political:
                            if isinstance(asset,Unit):
                                units.append(asset)
                        for asset in cur_nation.assets_force:
                            if isinstance(asset,Unit):
                                units.append(asset)
                        # Go through unit and find out if it belongs to a unitgroup already 
                        for unit in units:
                            for unitgroup in unitgroups:
                                if unit in unitgroup.unit_list:
                                    text+=f"{unit.uid} - {unit.nickname} - Part of: {unitgroup.nickname}\n"
                                    break
                                # If not in any unit group, it will print this instead \/
                                text+=f"{unit.uid} - {unit.nickname} - Unassigned\n"
                        await channel.send("Please select unit by ID:\nID--Name--Assignment")
                        await channel.send(text)

                        unitidchoice = int((await bot.wait_for("message",check=check)).content)
                        #Find the unit and then add it to the unit group, making sure it isnt in another one first
                        for unit in units:
                            if unit.uid == unitidchoice:
                                for unitgroup in unitgroups:
                                    if unit in unitgroup.unit_list:
                                        # Remove unit from unitgroup:
                                        unitgroup.unit_list.remove(unit)
                                        unitgroup.unit_id_list.remove(unit.uid)
                                        if unit.locked_unit != None: # Remove info about lockedunit
                                            unit.locked_unit.locked_unit_id=None
                                            unit.locked_unit.locked_unit=None
                                            unit.locked_unit=None
                                            unit.locked_unit_id=None
                            # Now add to new unitgroup
                            selected_unitgroup.add_unit(unit)
                                        

                    elif choice == 3: # Exit
                        ended = True



            else:
                await channel.send("Unable to find unit group")

        else:
            await channel.send("You must create a nation first!")
    except Exception as error:
        await channel.send(f"Error completing command: {error}")

@bot.command() #warmenu
async def warmenu(context:commands.Context):
    """ A command that allows the user to access the war menu, starting wars and assigning battlegroups to wars."""

    try:
        channel = context.message.channel
        author = context.author
        cur_nation = None
        
        def check(m:discord.Message)->bool: # Check used to validate input
            return(m.author == author)


        for nation in nation_list: # Find the player nation
            if nation.player_name == str(context.author.id):
                cur_nation = nation
        if cur_nation == None: # From this point on it can be assumed the player has a nation
            raise Exception("No player nation found, please sign up first.")

        await channel.send(
f"""
War Menu: Please type selected option\n
1. Start war
2. Manage wars
""")

        choice:int = int((await bot.wait_for('message',check=check)).content)
        if choice == 1:
            # Start war
            await channel.send("Please choose target nation by number\nNumber -- Nation Name\n")
            possible_nations:list[Nation] = []
            for nation in nation_list:
                if nation != cur_nation:
                    possible_nations.append(nation)
            text = ""
            i = 0
            if len(possible_nations) == 0:
                raise Exception("No nations available to target, you are possibly the only player playing.")
            for nation in possible_nations:
                text+=f"{i} - {nation.name}\n"
                i+=1
            await channel.send(text)
            indexchoice:int = int((await bot.wait_for('message',check=check)).content)
            if indexchoice<0 or indexchoice>=len(possible_nations):
                raise Exception("Nation selection out of range")
            target_nation = possible_nations[indexchoice]

            new_war = War()
            new_war.uid = nextWarID(war_list)
            new_war.aggressor_nation_uids.append(cur_nation.player_name)
            new_war.aggressor_nations.append(cur_nation)
            new_war.defender_nation_uids.append(target_nation.player_name)
            new_war.defender_nations.append(cur_nation)

            await channel.send("Type name of the war:")
            war_name:str = (await bot.wait_for('message',check=check)).content
            new_war.name = war_name

            war_list.append(new_war)

            await channel.send(f"Succesfully created {new_war.name} against {target_nation.name}")
        elif choice == 2:
            selectable_wars:list[War] = []
            for war in war_list:
                if cur_nation.player_name in war.aggressor_nation_uids or cur_nation.player_name in war.defender_nation_uids: # find all wars player is part of:
                    selectable_wars.append(war)
            if len(selectable_wars)==0:
                raise Exception("No wars to select.")
            await channel.send("Select war by index:\n Index -- War Name\n")
            text = ""
            i = 0
            for war in selectable_wars: # Lists out all wars player is part of
                text+=f"{i} - {war.name}\n"
                i+=1
            await channel.send(text)
            war_selection = int((await bot.wait_for('message',check=check)).content)
            if war_selection < 0 or war_selection >= len(selectable_wars):
                raise Exception("Selection is out of bounds\n")

            selected_war = selectable_wars[war_selection]
            await channel.send( # Opens up the menu for a selecter war
f"""
{selected_war.name} Menu Options:
1. Start a front
2. Manage fronts - Assign unit groups, view reports

""") 
            choice = int((await bot.wait_for('message',check=check)).content)
            if choice == 1: # Ability to start a new front
                await channel.send(
f"""
Select Front Battlespace: (Will only be able to use unit groups that can target this battlespace)
1. Ground
2. Air
3. Sea
4. Space
5. Cyber
6. Covert
7. Strategic
"""
                )
                battlespace_choice = int((await bot.wait_for('message',check=check)).content)
                if battlespace_choice < 1 or battlespace_choice >7:
                    raise Exception("Selection out of bounds\n")
                else:
                    new_front = Front()
                    if battlespace_choice == 1:
                        new_front.battlespace = "ground"
                    if battlespace_choice == 2:
                        new_front.battlespace = "air"
                    if battlespace_choice == 3:
                        new_front.battlespace = "sea"
                    if battlespace_choice == 4:
                        new_front.battlespace = "space"
                    if battlespace_choice == 5:
                        new_front.battlespace = "cyber"
                    if battlespace_choice == 6:
                        new_front.battlespace = "covert"
                    if battlespace_choice == 7:
                        new_front.battlespace = "strategic"
                # Pick a name for front
                await channel.send("Please name the front:")
                front_name = (await bot.wait_for('message',check=check)).content
                if len(front_name) == 0:
                    raise Exception("Front name cannot be empty.")
                # Instantiate the front
                new_front.name = front_name 
                new_front.uid = nextFrontID(front_list)
                selected_war.fronts.append(new_front)
                selected_war.front_uids.append(new_front.uid)
                front_list.append(new_front)
                await channel.send(f"Successfully started {new_front.name}")
            elif choice == 2: # Manage a front
                text = "Select front by index:\nIndex - Front Name\n"
                i = 0
                for front in selected_war.fronts:
                    text+=f"{i} - {front.name}"
                    i+=1
                await channel.send(text)
                indexchoice = int((await bot.wait_for('message',check=check)).content)
                if indexchoice < 0 or indexchoice >= len(selected_war.fronts):
                    raise Exception("Selection is out of bounds\n")
                selected_front = selected_war.fronts[indexchoice]
                await channel.send(
f"""{selected_front.name} Menu Options:
1. Add main unit group (1 max)
2. Add supporting unit group
3. View latest conflict log
""")
                choice = int((await bot.wait_for('message',check=check)).content)
                if choice == 1: # Add a main unit
                    #checks if there is already a unit group as the main group
                    if (cur_nation.player_name in selected_war.aggressor_nation_uids and selected_front.attacker_unit_group != None) or (cur_nation.player_name in selected_war.defender_nation_uids and selected_front.defender_unit_group != None):
                        raise Exception("There already is one main UnitGroup on your side")
                    # Goes through all unit groups and lists possible choices
                    potential_unitgroups:list[UnitGroup] = []
                    for asset in asset_list:
                        if isinstance(asset,UnitGroup):
                            # Checks if unit has the correct battlespace and belongs to the player and isnt supporting
                            if selected_front.battlespace in asset.attackable_battlespaces and (asset in cur_nation.assets_force or asset in cur_nation.assets_political or asset in cur_nation.assets_wealth) and asset.supporting != True:
                                potential_unitgroups.append(asset)
                    if len(potential_unitgroups) == 0:
                        raise Exception("No UnitGroups available")
                    text = "Select unit group to become your attacking/defending group by Index. \n Index - UnitGroup Name\n"
                    i = 0
                    for unitgroup in potential_unitgroups: # List out all possible unitgroups
                        text+=f"{i} - {unitgroup.nickname}\n"
                        i+=1
                    await channel.send(text)
                    indexchoice = int((await bot.wait_for('message',check=check)).content)
                    if indexchoice<0 or indexchoice>= len(potential_unitgroups):
                        raise Exception("Selection is out of bounds\n")
                    selected_unitgroup = potential_unitgroups[indexchoice]
                    # Check if unitgroup is already in another front
                    for front in front_list:
                        if selected_unitgroup in front.attack_support_unit_groups or selected_unitgroup in front.defend_support_unit_groups or selected_unitgroup == front.attacker_unit_group or selected_unitgroup == front.defender_unit_group:
                            raise Exception(f"Unit Group is already in front: {front.name}, to remove it from there, first finish the war on that front. ")

                    # Check which side unitgroup is on and add it
                    if cur_nation.player_name in selected_war.aggressor_nation_uids:
                        selected_front.attacker_unit_group = selected_unitgroup
                        selected_front.attacker_unit_group_id = selected_unitgroup.uid
                        channel.send(f"successfully added {selected_unitgroup.nickname} to {selected_front.name} as attacking unit group")
                    elif cur_nation.player_name in selected_war.defender_nation_uids:
                        selected_front.defender_unit_group = selected_unitgroup
                        selected_front.defender_unit_group_id = selected_unitgroup.uid
                        channel.send(f"successfully added {selected_unitgroup.nickname} to {selected_front.name} as defending unit group")
                elif choice == 2: # Add a supporting unit         
                    # Goes through all unit groups and lists possible choices
                    potential_unitgroups:list[UnitGroup] = []
                    for asset in asset_list:
                        if isinstance(asset,UnitGroup):
                            # Checks if unit has the correct battlespace and belongs to the player and is supporting
                            if selected_front.battlespace in asset.attackable_battlespaces and (asset in cur_nation.assets_force or asset in cur_nation.assets_political or asset in cur_nation.assets_wealth) and asset.supporting == True:
                                potential_unitgroups.append(asset)
                    if len(potential_unitgroups) == 0:
                        raise Exception("No UnitGroups available")
                    text = "Select unit group to add to supporting unit groups by Index. \n Index - UnitGroup Name\n"
                    i = 0
                    for unitgroup in potential_unitgroups: # List out all possible unitgroups
                        text+=f"{i} - {unitgroup.nickname}\n"
                        i+=1
                    await channel.send(text)
                    indexchoice = int((await bot.wait_for('message',check=check)).content)
                    if indexchoice<0 or indexchoice>= len(potential_unitgroups):
                        raise Exception("Selection is out of bounds\n")
                    selected_unitgroup = potential_unitgroups[indexchoice]
                    # Check if unitgroup is already in another front
                    for front in front_list:
                        if selected_unitgroup in front.attack_support_unit_groups or selected_unitgroup in front.defend_support_unit_groups or selected_unitgroup == front.attacker_unit_group or selected_unitgroup == front.defender_unit_group:
                            raise Exception(f"Unit Group is already in front: {front.name}, to remove it from there, first finish the war on that front. ")

                    # Check which side unitgroup is on and add it
                    if cur_nation.player_name in selected_war.aggressor_nation_uids:
                        selected_front.attack_support_unit_groups.append(selected_unitgroup)
                        selected_front.attack_support_unit_group_ids.append(selected_unitgroup.uid)
                        channel.send(f"successfully added {selected_unitgroup.nickname} to {selected_front.name} as attacker supporting unit group")
                    elif cur_nation.player_name in selected_war.defender_nation_uids:
                        selected_front.defend_support_unit_groups.append(selected_unitgroup)
                        selected_front.defend_support_unit_group_ids.append(selected_unitgroup.uid)
                        channel.send(f"successfully added {selected_unitgroup.nickname} to {selected_front.name} as defender supporting unit group")
                elif choice == 3: # Send latest log
                    await channel.send(selected_front.latestlog)


    except Exception as error:
        await channel.send(f"Error completing command: {error}")

@bot.command()
@commands.is_owner()
async def shutdown(context:commands.Context):
    status_channel = bot.get_channel(1138473460868317254)
    with open("logs.txt","a") as file:
        main.save_assets(asset_list)
        file.write("Assets Saved\n")
        main.save_wars(war_list)
        file.write("Wars Saved\n")
        main.save_fronts(front_list)
        file.write("Fronts Saved\n")
        main.save_nations(nation_list)
        file.write("Nations Saved\n")
        file.write(f"shutting down at {time.ctime(time.time())}\n")
    await status_channel.send(f"Shutting down at {time.ctime(time.time())}")
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
    
    
@bot.command() # taketurn
async def taketurn(context: commands.Context):
    channel = context.channel
    for nation in nation_list:
        if nation.player_name == str(context.author.id):
            nation.take_turn()

@bot.event
async def on_ready():
    status_channel = bot.get_channel(1138473460868317254)
    with open("logs.txt","a") as file:
        main.load_assets(asset_list)
        assetStore.nextID()
        await status_channel.send("Asset Loading Complete")
        file.write("Assets Loaded\n")
        main.load_nations(nation_list,asset_list)
        await status_channel.send("Nation Loading Complete")
        file.write("Nations Loaded\n")
        main.load_fronts(front_list,asset_list)
        await status_channel.send("Front Loading Complete")
        file.write("Fronts Loaded\n")
        main.load_wars(war_list,nation_list,front_list)
        await status_channel.send("War Loading Complete")
        file.write("Wars Loaded\n")
        await status_channel.send(f"Bot finished initialising at {time.ctime(time.time())}")
        file.write(f"Bot finished initialising at {time.ctime(time.time())}\n")
        # task1 = asyncio.create_task(timer())
        # await task1

async def timer():
    """ Can be used as a timer coroutine to make a turn happen every 24 hours """
    status_channel = bot.get_channel(1138473460868317254)
    await asyncio.sleep(60*60*24)
    await status_channel.send(f"Timer has passed at {time.ctime(time.time())}\n")

#if __name__ == "__main__":
#  asyncio.run(runner(bot))

bot.run(TOKEN)