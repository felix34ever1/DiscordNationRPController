import asset

def create_asset(new_asset:dict,asset_list:list):
    
    # Get asset type
    if new_asset["name"] == "Industrial Processing Plant":
        asset_object = asset.IPP()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    if new_asset["name"] == "Petroleum Plant":
        asset_object = asset.PP()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)