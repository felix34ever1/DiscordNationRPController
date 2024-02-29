import main
import nation
import asset
import assethandler

### Careful running as it could change asset.json or if errors, cause other problems 

asset_list = []
nation_list = []
assetStore = assethandler.AssetStore(asset_list)
new_nation = nation.Nation()
nation_list.append(new_nation)
new_nation.urban_population = 300000000
new_nation.capital_current = 300000000

main.load_assets(asset_list)
assetStore.nextID()
main.load_nations(nation_list,asset_list)
a = asset.LP()