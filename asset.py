### Asset class, <<<<Maybe>>>> all Asset subclasses are contained within the economy, political or force script. 

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

# Needed asset types: 
# DirectedAsset (able to target both the owner nation and target nation
# UnitGroup (holds units)
# Unit (Acts like a unit)

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
        if new_nation.production>=1 and new_nation.capital>25000000 and new_nation.wealth_number>=self.tier:
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
        if new_nation.production>=1 and new_nation.capital>50000000 and new_nation.wealth_number>=self.tier:
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

import nation