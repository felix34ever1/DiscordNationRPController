import main
import nation
from asset import Asset
import assethandler

asset_list = []
nation_list = []
assetStore = assethandler.AssetStore()
new_nation = nation.Nation()
nation_list.append(new_nation)
new_nation.urban_population = 300000000
new_nation.capital_current = 300000000

main.load_assets(asset_list)
assetStore.idpointer = len(asset_list)

selected_asset = assetStore.wealth_assets["Industrial Processing Plant"]
created_asset:Asset = selected_asset()
if created_asset.cost_calculation(new_nation): # Check if can add to nation
    created_asset.uid = assetStore.idpointer
    assetStore.idpointer+=1
    created_asset.append_to_nation(new_nation)
    asset_list.append(created_asset)


main.save_assets(asset_list)
