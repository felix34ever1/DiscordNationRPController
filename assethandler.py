from asset import Asset


def create_asset(asset:dict,asset_list:list):
    
    # Get asset type
    if asset["name"] == "Industrial Processing Plant":
        asset_object = Asset()
        asset_object.load_asset(asset)
        asset_list.append(asset_object)