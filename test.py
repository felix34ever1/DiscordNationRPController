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


# infantry
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

# aircraft
planes1 = asset.TacticalWing()
planes1.nickname = "1st Royal Wings"
planes2 = asset.TacticalWing()
planes2.nickname = "2nd Royal Wings"
planes3 = asset.TacticalWing()
planes3.nickname = "3st Royal Wings"
planes4 = asset.TacticalWing()
planes4.nickname = "4nd Royal Wings"

# naval
cruiser = asset.Cruiser()
destroyer = asset.Destroyer()

# weapons
bombs = asset.Weapon()
bombs.damage_soft = 5.0
bombs.possible_battlespaces.append("ground")

cannonnaval = asset.Weapon()
cannonnaval.naval_damage = 5
cannonnaval.naval_ap = 5
cannonnaval.possible_battlespaces.append("naval")

aagun = asset.Weapon()
aagun.air_attack = 2.0
aagun.possible_battlespaces.append("air")

planes1.weapon_list.append(bombs)
bombs.owner_unit = planes1

cruiser.weapon_list.append(cannonnaval)
cruiser.weapon_list.append(cannonnaval)

destroyer.weapon_list.append(cannonnaval)

unit_list:list[asset.Unit] = [inf,inf2,inf3,inf4,inf5,inf6,planes1,planes2,planes3,planes4]

unitgroup1 = asset.UnitGroup()
unitgroup1.unit_list.append(inf)
unitgroup1.unit_list.append(inf2)
unitgroup1.unit_list.append(inf3)
unitgroup2 = asset.UnitGroup()
unitgroup2.unit_list.append(inf4)
unitgroup2.unit_list.append(inf5)
unitgroup2.unit_list.append(inf6)
unitgroup2.enemy_unit_group = unitgroup1
unitgroup3 = asset.UnitGroup()
unitgroup3.supporting = True
unitgroup3.allied_unit_group = unitgroup1
unitgroup3.unit_list.append(planes1)
unitgroup3.unit_list.append(planes2)
unitgroup4 = asset.UnitGroup()
unitgroup4.allied_unit_group = unitgroup2
unitgroup4.unit_list.append(planes1)
unitgroup4.unit_list.append(planes2)

unitgroup1.enemy_unit_group = unitgroup2
unitgroup3.allied_unit_group = unitgroup1
unitgroup1.fight_type = "pairup"
unitgroup3.fight_type = "randomall"
#unitgroup3.fight_length = 5
#unitgroup1.attack()
unitgroup1.attack()
unitgroup1.fought_this_turn = False
unitgroup2.fought_this_turn = False

for unit in unit_list:
    print(unit.display())

unitgroup1.attack()
print("--------Turn 2----------")

for unit in unit_list:
    print(unit.display())