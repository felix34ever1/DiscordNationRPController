import json
from nation import Nation
from asset import Asset,Unit,UnitGroup
from war import War,Front
import assethandler



### Loading Procedure:
# 1. Put all assets json into a list
# 2. Convert asset json into asset objects using an asset converter script and store them in three lists (wealth,political,force)
# 3. Load all nations into a nation masterlist.
# 4. Hook up assets to nations.
# 5. Calculate all nation statistics.

### Saving procedure:
# 1. id each asset and save the ids of all assets in the nation.
# 2. convert all assets to json using converter script. Save to file
# 3. convert all nations to json. Save to file



def load_assets(asset_list:list):
    """Takes a list and loads it with Asset objects from the json savefile"""
    asset_file = open("asset.json","r")
    asset_text = asset_file.read()

    imported_assets = json.loads(asset_text)
    for asset_json in imported_assets["list"]:
        assethandler.create_asset(asset_json,asset_list)

    asset_file.close()

    # Now handle loading units to unit groups
    for potentialgroup in asset_list:
        if isinstance(potentialgroup,UnitGroup):
            for potentialunit in asset_list:
                if isinstance(potentialunit,Unit):
                    if potentialunit.uid in potentialgroup.unit_id_list:
                        potentialgroup.unit_list.append(potentialunit)

def load_wars(war_list:list[War],nation_list:list[Nation],front_list:list[Front]):
    """Takes a list and loads it with War objects from the json savefile"""
    with open("war.json","r") as war_file:
        war_text = war_file.read()

        imported_wars = json.loads(war_text)
        for war_json in imported_wars["list"]:
            new_war = War()
            new_war.load_war(war_json)
            new_war.hook_nations(nation_list)
            new_war.hook_fronts(front_list)
            war_list.append(new_war)
            

def load_fronts(front_list:list[Front],asset_list:list[Asset]):
    """Takes a list and loads it with Front objects from the json savefile"""
    with open("front.json","r") as front_file:
        front_text = front_file.read()

        imported_fronts = json.loads(front_text)
        for front_json in imported_fronts["list"]:
            new_front = Front()
            new_front.load_front(front_json)
            new_front.hook_unit_groups(asset_list)
            front_list.append(new_front)

def load_nations(nation_list:list,asset_list:list):
    """Takes a list and loads it with Nation objects from the json savefile"""
    
    with open("nation.json","r") as nation_file:
        nation_text = nation_file.read()

        imported_nations = json.loads(nation_text)
        for nation_json in imported_nations["list"]:
            new_nation = Nation()
            new_nation.import_data(nation_json)
            new_nation.hook_assets(asset_list)
            nation_list.append(new_nation)
        
        
    
def save_assets(asset_list:list[Asset]):
    """Save assets into json file :)"""
    save_data = {"list":[]}
    
    for asset in asset_list: # Extract all data into one list
        asset_save_data = asset.export_asset()
        save_data["list"].append(asset_save_data)

    save_data_json = json.dumps(save_data,indent=4) # turns python data to a json
    with open("asset.json","w") as file: # open json file
        file.write(save_data_json)

def save_wars(war_list:list[War]):
    """Save wars into json file :)"""
    save_data = {"list":[]}
    
    for war in war_list: # Extract all data into one list
        war_save_data = war.export_war()
        save_data["list"].append(war_save_data)

    save_data_json = json.dumps(save_data,indent=4) # turns python data to a json
    with open("war.json","w") as file: # open json file
        file.write(save_data_json)

def save_fronts(front_list:list[Front]):
    """Save fronts into json file so epic"""
    save_data = {"list":[]}
    for front in front_list: # Extract all data into one list
        front_save_data = front.export_front()
        save_data["list"].append(front_save_data)
    save_data_json = json.dumps(save_data,indent=4) # Turns python data to json
    with open("front.json","w") as file:
        file.write(save_data_json)

def save_nations(nation_list: list[Nation]):
    """Saves all the nations from a list of nations to a json file"""
    save_data = {"list":[]}
    for nation in nation_list:
        nation_save_data = nation.export_data()
        save_data["list"].append(nation_save_data)
    save_data_json = json.dumps(save_data,indent=4) # Turns python data type to a json formatted string
    with open("nation.json","w") as file:# Opens the json file
        file.write(save_data_json) # Writes json string into the file
    



nation_list:list[Nation] = []
asset_list = []

