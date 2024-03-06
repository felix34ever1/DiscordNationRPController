import random
import copy
### Asset class, <<<<Maybe>>>> all Asset subclasses are contained within the economy, political or force script. 

# Needed asset types: 
# Ability (Performs an action and then can delete itself)
# DirectedAbility (Performs an action and can hold a target nation)
# DirectedAsset (able to target both the owner nation and target nation)
# UnitGroup (holds units)
# Unit (Acts like a unit)

class Asset():

    def __init__(self):
        """Creates an Asset, this is the parent class for all assets and assets should set their own cost_calculation, building_purchase, upkeep and production functions if needed"""
        self.uid = -1 # Unique Identifier
        self.name = "" # Name of the asset e.g refinery or bank etc.
        self.type = "" # Wealth, Political or Force
        self.tier = 1 # How high the country has to have a level in the type 
        self.construction_time = 0 # The amount of turns left until it finishes building (0 if complete)
        self.activated = True
        
        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.has_hooked = False

    def hook(self,owner_nation):
        self.owner_nation:nation.Nation = owner_nation
        self.has_hooked = True

    def load_asset(self,json_data:dict):
        """ Takes json data in the form of a dictionary and loads its properties from there"""
        self.uid = json_data["uid"]
        self.name = json_data["name"]
        self.type = json_data["type"]
        self.construction_time = json_data["construction time"]

    def export_asset(self)->dict:
        """Turn the asset into json data to be exported, returns a dictionary"""
        json_data = {}
        json_data["uid"] = self.uid
        json_data["name"] = self.name
        json_data["type"] = self.type
        json_data["construction time"] = self.construction_time
        return(json_data)

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        return False

    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        # costs go here
        self.append_to_nation(new_nation)

    def build(self):
        """If the asset hasn't fully finished building yet, it can now build itself"""
        if self.construction_time>0:
            self.construction_time-=1

    def append_to_nation(self,new_nation):
        new_nation:nation.Nation = new_nation
        self.owner_nation = new_nation
        self.hook(new_nation)
        if self.type == "wealth":
            new_nation.assets_wealth_id.append(self.uid)
            new_nation.assets_wealth.append(self)
        elif self.type == "political":
            new_nation.assets_political_id.append(self.uid)
            new_nation.assets_political.append(self)
        elif self.type == "force":
            new_nation.assets_force_id.append(self.uid)
            new_nation.assets_force.append(self)

    def delete_self(self):
        """ Remove the asset and mention of it from anywhere. """
        if self.has_hooked:
            if self.type == "wealth":
                self.owner_nation.assets_wealth_id.remove(self.uid)
                self.owner_nation.assets_wealth.remove(self)
            elif self.type == "political":
                self.owner_nation.assets_political_id.remove(self.uid)
                self.owner_nation.assets_political.remove(self)
            elif self.type == "force":
                self.owner_nation.assets_force_id.remove(self.uid)
                self.owner_nation.assets_force.remove(self)
        
        del self

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def upkeep(self):
        """Called at the end of turn to calculate consumption taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")
    
    def alter_nation_metrics(self):
        """Called to change stability or economic strength of nation"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def get_uid(self)->int:
        """Returns the Unique Identifier of the asset"""
        return(self.uid)

class DirectedAsset(Asset):
    def __init__(self):
        """Creates an Asset, this is the parent class for all assets and assets should set their own cost_calculation, building_purchase, upkeep and production functions if needed"""
        self.uid = -1 # Unique Identifier
        self.name = "" # Name of the asset e.g refinery or bank etc.
        self.type = "" # Wealth, Political or Force
        self.tier = 1 # How high the country has to have a level in the type 
        self.construction_time = 0 # The amount of turns left until it finishes building (0 if complete)
        self.activated = True
        
        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.target_nation = None # Assigned to targeted nation by the directed asset.
        self.target_nation_id = "" # ID of the target nation
        self.has_hooked = False

    def hook(self,hooking_nation):
        """Take a nation that is hooking to asset and try to decide if """
        hooking_nation:nation.Nation = hooking_nation
        if hooking_nation.player_name == self.target_nation_id: # check if hooking nation is target or owner
            self.target_nation = hooking_nation
        else:
           self.owner_nation:nation.Nation = hooking_nation
        self.has_hooked = True

    def building_purchase(self,new_nation,target_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        # costs go here
        self.append_to_nation(new_nation,target_nation)

    def load_asset(self,json_data:dict):
        """ Takes json data in the form of a dictionary and loads its properties from there"""
        self.uid = json_data["uid"]
        self.name = json_data["name"]
        self.type = json_data["type"]
        self.construction_time = json_data["construction time"]
        self.target_nation_id = json_data["target nation id"]

    def export_asset(self)->dict:
        """Turn the asset into json data to be exported, returns a dictionary"""
        json_data = {}
        json_data["uid"] = self.uid
        json_data["name"] = self.name
        json_data["type"] = self.type
        json_data["construction time"] = self.construction_time
        json_data["target nation id"] = self.target_nation_id
        return(json_data)

    def append_to_nation(self,new_nation,target_nation):
        new_nation:nation.Nation = new_nation
        target_nation:nation.Nation = target_nation
        self.owner_nation = new_nation
        self.target_nation = target_nation
        self.target_nation_id = self.target_nation.player_name
        self.hook(new_nation)
        if self.type == "wealth":
            new_nation.assets_wealth_id.append(self.uid)
            new_nation.assets_wealth.append(self)
            target_nation.assets_wealth_id.append(self.uid)
            target_nation.assets_wealth.append(self)
        elif self.type == "political":
            new_nation.assets_political_id.append(self.uid)
            new_nation.assets_political.append(self)
            target_nation.assets_political_id.append(self.uid)
            target_nation.assets_political.append(self)
        elif self.type == "force":
            new_nation.assets_force_id.append(self.uid)
            new_nation.assets_force.append(self)
            target_nation.assets_force_id.append(self.uid)
            target_nation.assets_force.append(self)

    def delete_self(self):
        """ Remove the asset and mention of it from anywhere. """
        if self.has_hooked:
            if self.type == "wealth":
                self.owner_nation.assets_wealth_id.remove(self.uid)
                self.owner_nation.assets_wealth.remove(self)
                self.target_nation.assets_wealth_id.remove(self.uid)
                self.target_nation.assets_wealth.remove(self)
            elif self.type == "political":
                self.owner_nation.assets_political_id.remove(self.uid)
                self.owner_nation.assets_political.remove(self)
                self.target_nation.assets_political_id.remove(self.uid)
                self.target_nation.assets_political.remove(self)
            elif self.type == "force":
                self.owner_nation.assets_force_id.remove(self.uid)
                self.owner_nation.assets_force.remove(self)
                self.target_nation.assets_force_id.remove(self.uid)
                self.target_nation.assets_force.remove(self)
        
        del self

class Ability(Asset):

    def __init__(self,asset_list:list=[]):
        super().__init__()
        self.asset_list = asset_list

    def delete_self_removelink(self):
        """ Remove the asset and mention of it from anywhere, as an ability, it can remove itself from the asset_list when needed. """
        if self.has_hooked:
            if self.type == "wealth":
                self.owner_nation.assets_wealth_id.remove(self.uid)
                self.owner_nation.assets_wealth.remove(self)
            elif self.type == "political":
                self.owner_nation.assets_political_id.remove(self.uid)
                self.owner_nation.assets_political.remove(self)
            elif self.type == "force":
                self.owner_nation.assets_force_id.remove(self.uid)
                self.owner_nation.assets_force.remove(self)

        self.asset_list.remove(self)
        
        del self

class DirectedAbility(DirectedAsset):
    def __init__(self,asset_list:list=[]):
        """Creates an Asset, this is the parent class for all assets and assets should set their own cost_calculation, building_purchase, upkeep and production functions if needed"""
        self.uid = -1 # Unique Identifier
        self.name = "" # Name of the asset e.g refinery or bank etc.
        self.type = "" # Wealth, Political or Force
        self.tier = 1 # How high the country has to have a level in the type 
        self.construction_time = 0 # The amount of turns left until it finishes building (0 if complete)
        self.activated = True
        
        self.asset_list = asset_list

        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.target_nation = None # Assigned to targeted nation by the directed asset.
        self.target_nation_id = "" # ID of the target nation
        self.has_hooked = False

    def delete_self_removelink(self):
        """ Remove the asset and mention of it from anywhere, as an ability, it can remove itself from the asset_list when needed. """
        if self.has_hooked:
            self.owner_nation:nation.Nation
            self.target_nation:nation.Nation
            if self.type == "wealth":
                self.owner_nation.assets_wealth_id.remove(self.uid)
                self.owner_nation.assets_wealth.remove(self)
                self.target_nation.assets_wealth_id.remove(self.uid)
                self.target_nation.assets_wealth.remove(self)
            elif self.type == "political":
                self.owner_nation.assets_political_id.remove(self.uid)
                self.owner_nation.assets_political.remove(self)
                self.target_nation.assets_political_id.remove(self.uid)
                self.target_nation.assets_political.remove(self)
            elif self.type == "force":
                self.owner_nation.assets_force_id.remove(self.uid)
                self.owner_nation.assets_force.remove(self)
                self.target_nation.assets_force_id.remove(self.uid)
                self.target_nation.assets_force.remove(self)

        self.asset_list.remove(self)
        
        del self

# Unit fighting procedures
        # Battlegroups will decide which units are fighting which.
        # Units should figure out 

class UnitGroup(DirectedAsset): 
    #IMPROVEMENT: Need a way to decide which units are / aren't allowed inside which groups
    def __init__(self):
        """Creates a unit group, can store a target unit or target nation but does not need it assigned. """
        self.uid = -1 # Unique Identifier
        self.name = "" # Name of the asset e.g refinery or bank etc.
        self.type = "" # Wealth, Political or Force
        self.tier = 1 # How high the country has to have a level in the type 
        self.construction_time = 0 # The amount of turns left until it finishes building (0 if complete)
        self.activated = True

        self.supporting:int = False # Used to decide if this does attack function or support function. Supporting assets don't take direct damage or have an auxilliary idea, e.g CAS/recon. Should not be given to units like infantry or tanks or ships unless ships are performing coastal bombardment.
        self.fight_length:int = 1 # This determines how long a fight lasts each turn. 
        self.fight_type:str = "pairup" # Type:
        #- pairup(each unit pairs up with an enemy, unpaired units don't attack but increase advantage),
        #- randomall(all units randomly pick an enemy unit to attack, multiple units can pick the same) 

        self.attack_type = ""
        self.unit_list:list[Unit] = []
        self.unit_id_list:list[int] = []
        self.enemy_unit_group:UnitGroup = None
        self.allied_unit_group:UnitGroup = None

        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.target_nation = None # Assigned to targeted nation by the directed asset.
        self.target_nation_id = "" # ID of the target nation
        self.has_hooked = False

    def attack(self)->str:
        if self.enemy_unit_group != None: # Check there are units in the enemy group
            enemy_units:list[Unit] = []
            enemy_units = (self.enemy_unit_group.unit_list).copy() # Shallow copies the lists so that elements can be removed for pairing purposes
            unit_list = self.unit_list.copy()

            # Go through each unit and select an opponent
            if self.fight_type == "pairup":
                for unit in unit_list:  
                    # First check if the unit is already locked with a valid unit, if so, remove valid unit from list
                    if unit.locked_unit != None:
                        if unit.locked_unit in enemy_units: # Remove enemy unit from list
                            enemy_units.remove(unit.locked_unit)
                        else:
                            unit.locked_unit = None
                    
                for unit in unit_list:  # Now actually select the opponent if not already got one
                    if len(enemy_units) == 0 or unit.locked_unit != None: # Makes sure you're not trying to fight a size 0 army or that the unit is already locked.
                            break
                    else:
                        unit_index = random.randint(0,len(enemy_units)-1)
                        unit.locked_unit = enemy_units.pop(unit_index)
                        unit.locked_unit.locked_unit = unit

                for unit in self.unit_list: 
                    # Loops through each unit and resolves attacks, for both the unit and the unit it is engaged to.
                    if unit.locked_unit != None:
                        enemy_unit = unit.locked_unit
                        if unit.recon_bonus>enemy_unit.recon_bonus:
                            if unit.check_battlespace(enemy_unit):
                                unit.attack(enemy_unit)
                            if enemy_unit.check_battlespace(unit):
                                enemy_unit.attack(unit)
                        else:
                            if enemy_unit.check_battlespace(unit):
                                enemy_unit.attack(unit)
                            if unit.check_battlespace(enemy_unit):
                                unit.attack(enemy_unit)
            
            elif self.fight_type == "randomall":
                for unit in unit_list: 
                    if len(enemy_units) == 0: # Makes sure you're not trying to fight a size 0 army or that the unit is already locked.
                            break
                    else:
                        unit_index = random.randint(0,len(enemy_units)-1)
                        unit.locked_unit = enemy_units[unit_index]
                
                for enemy in enemy_units: 
                    if len(enemy_units) == 0: # Makes sure you're not trying to fight a size 0 army or that the unit is already locked.
                            break
                    else:
                        unit_index = random.randint(0,len(unit_list)-1)
                        enemy.locked_unit = unit_list[unit_index]

            unit_attack_queue:list[Unit] = [] # Used for determining unit order, if a unit has better recon than its opponent, it executes, otherwise it is added to this list to be executed after

            for unit in unit_list:
                if unit.recon_bonus > unit.locked_unit.recon_bonus:
                    if unit.check_battlespace(unit.locked_unit):
                        unit.attack(unit.locked_unit)
                else:
                    unit_attack_queue.append(unit)
            
            for unit in enemy_units:
                if unit.recon_bonus > unit.locked_unit.recon_bonus:
                    if unit.check_battlespace(unit.locked_unit):
                        unit.attack(unit.locked_unit)
                else:
                    unit_attack_queue.append(unit)
            
            for unit in unit_attack_queue:
                if unit.check_battlespace(unit.locked_unit):
                    unit.attack(unit.locked_unit)
                
        else:
            return len(self.unit_list) # Else return the number of units as a sort of occupation amount

    def support(self):
        if self.allied_unit_group != None:
        # Check if the attached unit group has an enemy
            if self.allied_unit_group.enemy_unit_group != None:
                enemy_unit_group = self.allied_unit_group.enemy_unit_group
                enemy_units = enemy_unit_group.unit_list.copy()
                unit_list = self.unit_list.copy()

                for unit in unit_list:
                    unit.locked_unit = None

                # Assign randomly how to fight the enemies, without provoking retaliation.
                if self.fight_type == "pairup":
                    for unit in unit_list:
                        if len(enemy_units) == 0:
                            break
                        else:
                            unit_index = random.randint(0,len(enemy_units)-1)
                            unit.locked_unit = enemy_units.pop(unit_index)
                elif self.fight_type == "randomall":
                    for unit in unit_list:
                        if len(enemy_units) == 0:
                            break
                        else:
                            unit_index = random.randint(0,len(enemy_units)-1)
                            unit.locked_unit = enemy_units[unit_index]
                
                for unit in unit_list:
                    if unit.locked_unit!=None:
                        if unit.check_battlespace(unit.locked_unit):
                            unit.attack(unit.locked_unit)

class Unit(Asset):
    def __init__(self):
        """Creates a Unit, usually a military group able to engage in combat. It will contain many properties based off of what it can do."""
        self.uid = -1 # Unique Identifier
        self.name = "" # Name of the unit e.g refinery or bank etc.
        self.nickname = "" # Player assigned name
        self.type = "" # Wealth, Political or Force
        self.battlespace:str = ""
        self.possible_battlespaces:list[str] = [] # Possible attack target battlespaces
        self.battlespace_list:list[str] = [] # a list holding all of the battlespaces that the unit counts as being in.
        self.tier = 1 # How high the country has to have a level in the type 
        self.construction_time = 0 # The amount of turns left until it finishes building (0 if complete)
        self.activated = True
        
        ## Unit stats
        self.locked_unit:Unit = None
        self.compels_reaction:bool = False # This tells if the unit makes the enemy attack it.
        
        # Unit Defences
        self.morale_max = 1.0 # The maximum amount of morale for a ground unit as well as cover ops units.
        self.armour = 0.0 # How much it reduces soft attack by. (Hard attack damage is capped to this) ground unit
        self.morale_current = self.morale_max

        self.dodge = 0.0 # Used by air units to avoid damage, incoming damage is timed by 1 - dodge. e.g dodge 0.1 reduces damage by 10%  
        self.air_integrity_max = 0.0 # Air health
        self.air_integrity_current = self.air_integrity_max #
        
        self.hull_health_max = 0.0 # Health of ships, does not reduce effectiveness of ship as it gets reduced
        self.naval_armour = 0.0 # Used to prevent damage from attacks. Otherwise doesn't reduce anything. 
        self.hull_health_current = self.hull_health_max

        self.orbital_defence = 0.0 # Used as a chance to avoid an attack.

        self.cyber_defence = 0.0 # Used to negate cyberattacks, if summed larger than cyber attacks, then it will negate it

        self.intelligence = 0.0 # Used to negate covert attacks.

        # Unit Attacks
        self.damage_soft = 0.0 # Damage it deals to unarmoured ground units
        self.damage_hard = 0.0 # Damage it deals to armoured ground units

        self.air_attack = 0.0 # Damage dealt to air units.

        self.naval_damage = 0.0 # Damage it deals to naval assets.
        self.naval_ap = 0.0 # How much naval armour it can pierce.
        
        self.orbital_attack = False # Determines if it can perform an orbital attack. All orbital attacks 1 hit kill enemy orbital units
        
        self.cyber_offense = 0.0 # Has to be higher than defender cyber defence.
        
        self.covert_ops_score = 0.0 # Determines if a unit succeeds a covert attack.

        self.recon_bonus = 0.0 # Used to determine if it attacks first

        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.has_hooked = False

    def attack(self,enemy_unit)->bool:
        enemy_unit:Unit = enemy_unit

        if enemy_unit.battlespace == "ground":
            damagesoft = self.damage_soft*(self.morale_current/self.morale_max) - enemy_unit.armour
            if damagesoft<0:
                damagesoft = 0
            damagehard = self.damage_hard*(self.morale_current/self.morale_max)
            if damagehard>enemy_unit.armour:
                damagehard = enemy_unit.armour
            enemy_unit.morale_current -= damagesoft+damagehard
        
        elif enemy_unit.battlespace == "air":
            enemy_unit.air_integrity_current -= self.air_attack*(1-enemy_unit.dodge)
        
        elif enemy_unit.battlespace == "naval":
            if enemy_unit.naval_armour<=self.naval_ap:
                enemy_unit.hull_health_current-=self.naval_damage

        elif enemy_unit.battlespace == "space" and self.orbital_attack:
            if random.random() > enemy_unit.orbital_defence:
                enemy_unit.kill_self()
                return True
            else:
                return False
        
        elif enemy_unit.battlespace == "cyber":
            if self.cyber_offense > enemy_unit.cyber_defence:
                return True
            else:
                return False
        
        elif enemy_unit.battlespace == "covert": # Possibly consider adding a critical failure condition
            if self.covert_ops_score > enemy_unit.intelligence:
                if self.covert_ops_score > enemy_unit.intelligence+5:
                    return True
                else:
                    self.morale_current-=enemy_unit.damage_soft*(enemy_unit.morale_current/enemy_unit.morale_max)
                    return True
            else:
                return False

        if self.compels_reaction:
            enemy_unit.attack(self)
            
    def check_battlespace(self,enemy)->bool:
        enemy:Unit = enemy
        if enemy.battlespace in self.possible_battlespaces:
            return True
        else:
            return False

    def kill_self(self):
        pass

    def display(self)->str:
        text = ""
        if self.battlespace == "ground":
            text = (
f'''
{self.nickname} --- {self.name}
MORALE: {self.morale_current}/{self.morale_max}
''')
        elif self.battlespace == "air":
            text = (    
f'''
{self.nickname} --- {self.name}
INTEGRITY: {self.air_integrity_current}/{self.air_integrity_max}
''')
        elif self.battlespace == "naval":
            text = (    
f'''
{self.nickname} --- {self.name}
HULL: {self.hull_health_current}/{self.hull_health_max}
''')
        if self.locked_unit != None:
            text+=f"Engaged: {self.locked_unit.nickname}"
        return text


######## WEALTH

class IPP(Asset):
    
    def __init__(self):
        """ Creates an Industrial Processing Plant Asset."""
        super().__init__()
        self.name = "Industrial Processing Plant"
        self.type = "wealth"
        self.tier = 1

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=3 and new_nation.capital>100000000 and new_nation.wealth_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=3
        new_nation.used_capital+=100000000
        self.construction_time = 2
        
        self.append_to_nation(new_nation)

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                self.owner_nation.industrial_metals_raw+=3
                self.owner_nation.resources_produced+=3
        else:
            print(f"Asset {self.uid} is unhooked ")

class PP(Asset):
    def __init__(self):
        """ Creates a Petroleum Plant"""
        super().__init__()
        self.name = "Petroleum Plant"
        self.type = "wealth"
        self.tier = 1

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=3 and new_nation.capital>150000000 and new_nation.wealth_number>=self.tier:
            return True
        return False

    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=3
        new_nation.used_capital+=150000000
        self.construction_time = 4
        
        self.append_to_nation(new_nation)

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                self.owner_nation.oil_raw+=3
                self.owner_nation.resources_produced+=3
        else:
            print(f"Asset {self.uid} is unhooked ")


    def upkeep(self):
        """Called at the end of turn to calculate consumption taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

class CI(Asset):
    def __init__(self):
        """ Creates a Consumer Industry"""
        super().__init__()
        self.name = "Consumer Industry"
        self.type = "wealth"
        self.tier = 1

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=2 and new_nation.capital>50000000 and new_nation.wealth_number>=self.tier:
            return True
        return False

    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=2
        new_nation.used_capital+=50000000
        self.construction_time = 2
        
        self.append_to_nation(new_nation)

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0 and self.owner_nation.industrial_metals_raw >= 2:
                self.owner_nation.industrial_metals_raw -= 2
                self.owner_nation.consumer_products_raw += 1
                self.owner_nation.resources_spent +=2
                self.owner_nation.resources_produced += 1
                self.activated = True
            else:
                self.activated = False
        else:
            print(f"Asset {self.uid} is unhooked ")


    def upkeep(self):
        """Called at the end of turn to calculate consumption taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

class RMR(Asset):
    def __init__(self):
        """ Creates a Rare Metals Refinery Asset."""
        super().__init__()
        self.name = "Rare Metals Refinery"
        self.type = "wealth"
        self.tier = 2

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=3 and new_nation.capital>200000000 and new_nation.wealth_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=3
        new_nation.used_capital+=200000000
        self.construction_time = 3
        
        self.append_to_nation(new_nation)

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                self.owner_nation.rare_metals_raw+=3
                self.owner_nation.resources_produced+=3
        else:
            print(f"Asset {self.uid} is unhooked ")    

class SPP(Asset):
    def __init__(self):
        """ Creates a Synthetic Plastic Plant Asset."""
        super().__init__()
        self.name = "Synthetic Plastic Plant"
        self.type = "wealth"
        self.tier = 2

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=2 and new_nation.capital>200000000 and new_nation.wealth_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=2
        new_nation.used_capital+=200000000
        self.construction_time = 2
        
        self.append_to_nation(new_nation)

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.owner_nation.oil_raw>=2:
                self.owner_nation.oil_raw-=2
                self.owner_nation.plastics_raw+=1
                self.owner_nation.resources_produced+=2
                self.owner_nation.resources_spent+=1
            else:
                self.activated = False
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

class EH(Asset):
    def __init__(self):
        """ Creates an Electronics Hub Asset."""
        super().__init__()
        self.name = "Electronics Hub"
        self.type = "wealth"
        self.tier = 2

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=4 and new_nation.capital>400000000 and new_nation.wealth_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=4
        new_nation.used_capital+=400000000
        self.construction_time = 6
        
        self.append_to_nation(new_nation)

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                if self.owner_nation.rare_metals_raw>=2:
                    self.owner_nation.electronics_raw+=2
                    self.owner_nation.rare_metals_raw-=2
                    self.owner_nation.resources_produced+=2
                    self.owner_nation.resources_spent+=2
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")    

class CD(Asset):
    def __init__(self):
        """ Creates an Civilian Development Asset."""
        super().__init__()
        self.name = "Civilian Development"
        self.type = "wealth"
        self.tier = 2

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=2 and new_nation.capital>80000000 and new_nation.wealth_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=2
        new_nation.used_capital+=80000000
        self.construction_time = 2
        
        self.append_to_nation(new_nation)

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                if self.owner_nation.plastics_raw>=1:
                    self.owner_nation.plastics_raw-=1
                    self.owner_nation.consumer_products_raw+=3
                    self.owner_nation.resources_spent+=1
                    self.owner_nation.resources_produced+=3

        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")      

######## POLITICAL

class SA(Asset):

    def __init__(self):
        super().__init__()
        self.name = "Solar Array"
        self.type = "political"
        self.tier = 1

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=3 and new_nation.capital>30000000 and new_nation.political_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=3
        new_nation.used_capital+=30000000
        self.construction_time = 1
        
        self.append_to_nation(new_nation)

    def upkeep(self):
        """Called at the end of turn to calculate consumption taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                self.owner_nation.power_raw+=1
        else:
            print(f"Asset {self.uid} is unhooked ")

class HD(Asset):

    def __init__(self):
        super().__init__()
        self.name = "Hydrostation Dam"
        self.type = "political"
        self.tier = 1

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=4 and new_nation.capital>100000000 and new_nation.political_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=4
        new_nation.used_capital+=100000000
        self.construction_time = 4
        
        self.append_to_nation(new_nation)

    def upkeep(self):
        """Called at the end of turn to calculate consumption taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                self.owner_nation.power_raw+=5
        else:
            print(f"Asset {self.uid} is unhooked ")

class LP(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Labour Programme"
        self.type = "political"
        self.tier = 1

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.capital>100000000 and new_nation.political_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_capital+=100000000
        self.construction_time = 1
        
        self.append_to_nation(new_nation)

    def upkeep(self):
        """Called at the end of turn to calculate consumption taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time > 0:
                self.owner_nation.production_raw+=1
            elif self.construction_time == 0:
                self.delete_self_removelink()
        else:
            print(f"Asset {self.uid} is unhooked ")

class SP(DirectedAbility):
    def __init__(self,asset_list:list=[]):
        """Created a Subversive Politics, an ability"""
        self.uid = -1 # Unique Identifier
        self.name = "Subversive Politics" # Name of the asset e.g refinery or bank etc.
        self.type = "political" # Wealth, Political or Force
        self.tier = 2 # How high the country has to have a level in the type 
        self.construction_time = 1 # The amount of turns left until it finishes building (0 if complete)
        self.activated = True
        
        self.asset_list = asset_list

        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.target_nation = None # Assigned to targeted nation by the directed asset.
        self.target_nation_id = "" # ID of the target nation
        self.has_hooked = False    

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.capital>100000000 and new_nation.political_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation,target_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_capital+=100000000
        self.construction_time = 1
        
        self.append_to_nation(new_nation,target_nation)

    def production(self):
        """Called at the end of turn to calculate consumption"""
        if type(self.target_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time > 0:
                self.target_nation.production_raw+=1
            elif self.construction_time == 0:
                self.delete_self_removelink()
            
        else:
            print(f"Asset {self.uid} is unhooked ")


######## FORCE

class MI(Asset):

    def __init__(self):
        super().__init__()
        self.name = "Military Industry"
        self.type = "force"
        self.tier = 1

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=2 and new_nation.capital>100000000 and new_nation.force_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=2
        new_nation.used_capital+=100000000
        self.construction_time = 2
        
        self.append_to_nation(new_nation)

    
    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0 and self.owner_nation.industrial_metals_raw>=2:
                self.owner_nation.industrial_metals_raw-=2
                self.owner_nation.military_products_raw+=1
                self.owner_nation.resources_spent+=2
                self.owner_nation.resources_produced+=1
                self.activated = True
            else:
                self.activated = False
        else:
            print(f"Asset {self.uid} is unhooked ")

class MES(Asset):
    def __init__(self):
        """ Creates an Manual Extraction Site Asset."""
        super().__init__()
        self.name = "Manual Extraction Site"
        self.type = "force"
        self.tier = 2

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=1 and new_nation.capital>25000000 and new_nation.force_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=1
        new_nation.used_capital+=25000000
        self.construction_time = 2
        
        self.append_to_nation(new_nation)

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            self.owner_nation.rare_metals_raw += 1
            self.owner_nation.resources_produced += 1
        else:
            print(f"Asset {self.uid} is unhooked ")     

    def alter_nation_metrics(self):
        """Called to change stability or economic strength of nation"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            self.owner_nation.predicted_political_stability-=2
            if self.owner_nation.predicted_political_stability<0:
                self.owner_nation.predicted_political_stability=0
        else:
            print(f"Asset {self.uid} is unhooked ")

class MOES(Asset):
    def __init__(self):
        """ Creates an Manual Oil Extraction Site Asset."""
        super().__init__()
        self.name = "Manual Oil Extraction Site"
        self.type = "force"
        self.tier = 2

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=1 and new_nation.capital>50000000 and new_nation.force_number>=self.tier:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=1
        new_nation.used_capital+=50000000
        self.construction_time = 2
        
        self.append_to_nation(new_nation)

    def secondary_production(self):
        """Checked after production to calculate if the building will be able to function, used by secondary industry"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            if self.construction_time == 0:
                pass
        else:
            print(f"Asset {self.uid} is unhooked ")

    def production(self):
        """Called at beginning of turn to calculate surplus taking the nation as a parameter"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            self.owner_nation.oil_raw += 1
            self.owner_nation.resources_produced += 1
        else:
            print(f"Asset {self.uid} is unhooked ")     

    def alter_nation_metrics(self):
        """Called to change stability or economic strength of nation"""
        if type(self.owner_nation) == nation.Nation: # Checks that the asset is hooked
            self.owner_nation.predicted_political_stability-=2
            if self.owner_nation.predicted_political_stability<0:
                self.owner_nation.predicted_political_stability=0
        else:
            print(f"Asset {self.uid} is unhooked ")

class InfantryBrigade(Unit):
    def __init__(self):
        """Creates an infantry brigade."""
        self.uid = -1 # Unique Identifier
        self.name = "Infantry Brigade" # Name of the unit e.g refinery or bank etc.
        self.nickname = "" # Player assigned name
        self.type = "force" # Wealth, Political or Force
        self.battlespace:str = "ground"
        self.possible_battlespaces:list[str] = ["ground"] # To attack
        self.battlespace_list:list[str] = ["ground"] # a list holding all of the battlespaces that the unit counts as being in.
        self.tier = 1 # How high the country has to have a level in the type 
        self.construction_time = 0 # The amount of turns left until it finishes building (0 if complete)
        self.activated = True
        
        ## Unit stats
        self.locked_unit:Unit = None
        self.compels_reaction:bool = False # This tells if the unit makes the enemy attack it.
        # Unit Defences
        self.morale_max = 10.0 # The maximum amount of morale for a ground unit as well as cover ops units.
        self.armour = 0.0 # How much it reduces soft attack by. (Hard attack damage is capped to this) ground unit
        self.morale_current = self.morale_max

        self.dodge = 0.0 # Used by air units to avoid damage, incoming damage is timed by 1 - dodge. e.g dodge 0.1 reduces damage by 10%  
        self.air_integrity_max = 0.0 # Air health
        self.air_integrity_current = self.air_integrity_max #
        
        self.hull_health_max = 0.0 # Health of ships, does not reduce effectiveness of ship as it gets reduced
        self.naval_armour = 0.0 # Used to prevent damage from attacks. Otherwise doesn't reduce anything. 
        self.hull_health_current = self.hull_health_max

        self.orbital_defence = 0.0 # Used as a chance to avoid an attack.

        self.cyber_defence = 0.0 # Used to negate cyberattacks, if summed larger than cyber attacks, then it will negate it

        self.intelligence = 0.0 # Used to negate covert attacks.

        # Unit Attacks
        self.damage_soft = 1.0 # Damage it deals to unarmoured ground units
        self.damage_hard = 0.0 # Damage it deals to armoured ground units

        self.air_attack = 0.1 # Damage dealt to air units.

        self.naval_damage = 0.0 # Damage it deals to naval assets.
        self.naval_ap = 0.0 # How much naval armour it can pierce.
        
        self.orbital_attack = False # Determines if it can perform an orbital attack. All orbital attacks 1 hit kill enemy orbital units
        
        self.cyber_offense = 0.0 # Has to be higher than defender cyber defence.
        
        self.covert_ops_score = 0.0 # Determines if a unit succeeds a covert attack.

        self.recon_bonus = 0.0 # Used to determine if it attacks first

        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.has_hooked = False

class TacticalWing(Unit):
    def __init__(self):
        """Creates a Unit, usually a military group able to engage in combat. It will contain many properties based off of what it can do."""
        self.uid = -1 # Unique Identifier
        self.name = "Tactical Wing" # Name of the unit e.g refinery or bank etc.
        self.nickname = "" # Player assigned name
        self.type = "force" # Wealth, Political or Force
        self.battlespace:str = "air"
        self.possible_battlespaces:list[str] = ["air","ground"]
        self.battlespace_list:list[str] = ["air"] # a list holding all of the battlespaces that the unit counts as being in.
        self.tier = 1 # How high the country has to have a level in the type 
        self.construction_time = 0 # The amount of turns left until it finishes building (0 if complete)
        self.activated = True
        
        ## Unit stats
        self.locked_unit:Unit = None
        self.compels_reaction:bool = True # This tells if the unit makes the enemy attack it.
        
        # Unit Defences
        self.morale_max = 1.0 # The maximum amount of morale for a ground unit as well as cover ops units.
        self.armour = 0.0 # How much it reduces soft attack by. (Hard attack damage is capped to this) ground unit
        self.morale_current = self.morale_max

        self.dodge = 0.3 # Used by air units to avoid damage, incoming damage is timed by 1 - dodge. e.g dodge 0.1 reduces damage by 10%  
        self.air_integrity_max = 2.0 # Air health
        self.air_integrity_current = self.air_integrity_max #
        
        self.hull_health_max = 0.0 # Health of ships, does not reduce effectiveness of ship as it gets reduced
        self.naval_armour = 0.0 # Used to prevent damage from attacks. Otherwise doesn't reduce anything. 
        self.hull_health_current = self.hull_health_max

        self.orbital_defence = 0.0 # Used as a chance to avoid an attack.

        self.cyber_defence = 0.0 # Used to negate cyberattacks, if summed larger than cyber attacks, then it will negate it

        self.intelligence = 0.0 # Used to negate covert attacks.

        # Unit Attacks
        self.damage_soft = 2.0 # Damage it deals to unarmoured ground units
        self.damage_hard = 2.0 # Damage it deals to armoured ground units

        self.air_attack = 0.5 # Damage dealt to air units.

        self.naval_damage = 0.0 # Damage it deals to naval assets.
        self.naval_ap = 0.0 # How much naval armour it can pierce.
        
        self.orbital_attack = False # Determines if it can perform an orbital attack. All orbital attacks 1 hit kill enemy orbital units
        
        self.cyber_offense = 0.0 # Has to be higher than defender cyber defence.
        
        self.covert_ops_score = 0.0 # Determines if a unit succeeds a covert attack.

        self.recon_bonus = 0.0 # Used to determine if it attacks first

        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.has_hooked = False
import nation