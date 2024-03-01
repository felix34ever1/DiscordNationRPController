import main
import nation
import asset
import assethandler

### Careful running as it could change asset.json or if errors, cause other problems 

asset_list = []
nation_list = []
assetStore = assethandler.AssetStore(asset_list,nation_list)
new_nation = nation.Nation()
nation_list.append(new_nation)
new_nation.political_number = 5
new_nation.urban_population = 300000000
new_nation.capital_current = 300000000
new_nation2 = nation.Nation()
nation_list.append(new_nation2)


main.load_assets(asset_list)
assetStore.nextID()
main.load_nations(nation_list,asset_list)

nation_text = "__Pick Target Nation by number:__\n"
for nation in nation_list:
    nation_text+=f"- {nation_list.index[nation]} - {nation.name}\n"
    
a = asset.SP()
assetStore.buy_directed_asset("Subversive Politics","political",new_nation,new_nation2)
print(new_nation.display())