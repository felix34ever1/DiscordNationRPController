import json
from nation import Nation


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

nation_list = []


def load_nations(nation_list:list):
    nation_file = open("nation.json","r")
    nation_text = nation_file.read()

    imported_assets = json.loads(nation_text)
    for nation_json in imported_assets["list"]:
        new_nation = Nation()
        new_nation.import_data(nation_json)
        nation_list.append(new_nation)
        new_nation.display()

load_nations(nation_list)