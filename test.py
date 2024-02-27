import main
import nation
from asset import Asset
import assethandler

### Careful running as it could change asset.json or if errors, cause other problems 

asset_list = []
nation_list = []
assetStore = assethandler.AssetStore()
new_nation = nation.Nation()
nation_list.append(new_nation)
new_nation.urban_population = 300000000
new_nation.capital_current = 300000000

main.load_assets(asset_list)
assetStore.idpointer = len(asset_list)
main.load_nations(nation_list,asset_list)
