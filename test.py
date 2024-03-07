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



inf = asset.InfantryBrigade()
inf.nickname = "1st Brigade"
inf2 = asset.InfantryBrigade()
inf2.nickname = "2nd Brigade"
inf3 = asset.InfantryBrigade()
inf3.nickname = "3rd Brigade"
inf4 = asset.InfantryBrigade()
inf4.nickname = "4th Brigade"
inf5 = asset.InfantryBrigade()
inf5.nickname = "5th Brigade"
inf6 = asset.InfantryBrigade()
inf6.nickname = "6th Brigade"
planes1 = asset.TacticalWing()
planes1.nickname = "1st Royal Wings"
planes2 = asset.TacticalWing()
planes2.nickname = "2nd Royal Wings"

unit_list:list[asset.Unit] = [inf,inf2,inf3,inf4,inf5,inf6,planes1,planes2]

unitgroup1 = asset.UnitGroup()
unitgroup1.unit_list.append(inf)
unitgroup1.unit_list.append(inf2)
unitgroup1.unit_list.append(inf3)
unitgroup2 = asset.UnitGroup()
unitgroup2.unit_list.append(inf4)
unitgroup2.unit_list.append(inf5)
unitgroup2.unit_list.append(inf6)
unitgroup3 = asset.UnitGroup()
unitgroup3.supporting = True
unitgroup3.allied_unit_group = unitgroup2
unitgroup2.enemy_unit_group = unitgroup1
unitgroup3.unit_list.append(planes1)
unitgroup3.unit_list.append(planes2)


unitgroup1.enemy_unit_group = unitgroup3
unitgroup1.fight_type = "pairup"
unitgroup3.fight_type = "pairup"
#unitgroup3.fight_length = 5
#unitgroup1.attack()
unitgroup3.support()

for unit in unit_list:
    print(unit.display())

unitgroup3.support()
#unitgroup3.support()

print("--------------------------")
for unit in unit_list:
    print(unit.display())

