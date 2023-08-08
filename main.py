import json
from nation import Nation
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

def load_nations(nation_list:list,asset_list:list):
    """Takes a list and loads it with Nation objects from the json savefile"""
    nation_file = open("nation.json","r")
    nation_text = nation_file.read()

    imported_nations = json.loads(nation_text)
    for nation_json in imported_nations["list"]:
        new_nation = Nation()
        new_nation.import_data(nation_json)
        new_nation.hook_assets(asset_list)
        nation_list.append(new_nation)
    

def save_nations(nation_list: list[Nation]):
    """Saves all the nations from a list of nations to a json file"""
    save_data = {"list":[]}
    for nation in nation_list:
        nation_save_data = nation.export_data()
        save_data["list"].append(nation_save_data)
    save_data_json = json.dumps(save_data,indent=4) # Turns python data type to a json formatted string
    file = open("nation.json","w") # Opens the json file
    file.write(save_data_json) # Writes json string into the file
    file.close()
    print(save_data)







