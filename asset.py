### Asset class, <<<<Maybe>>>> all Asset subclasses are contained within the economy, political or force script. 

class Asset():

    def __init__(self):
        """Creates an Asset, this is the parent class for all assets and assets should set their own cost_calculation, building_purchase, upkeep and production functions if needed"""
        self.uid = -1 # Unique Identifier
        self.name = "" # Name of the asset e.g refinery or bank etc.
        self.type = "" # Wealth, Political or Force
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

    def get_uid(self)->int:
        """Returns the Unique Identifier of the asset"""
        return(self.uid)

class IPP(Asset):
    
    def __init__(self):
        """ Creates an Industrial Processing Plant Asset."""
        super().__init__()
        self.name = "Industrial Processing Plant"
        self.type = "wealth"

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=3 and new_nation.capital>100000000:
            return True
        return False
    
    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=3
        new_nation.used_capital+=100000000
        self.construction_time = 2
        
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

    def cost_calculation(self,new_nation)->bool:
        """ Takes a nation that is trying to build it as a parameter and returns a bool if it can build it"""
        new_nation:nation.Nation = new_nation
        new_nation.economy_prediction()
        if new_nation.production>=3 and new_nation.capital>150000000:
            return True
        return False

    def building_purchase(self,new_nation):
        """ Takes the new nation that will build it and hooks to it."""
        new_nation:nation.Nation = new_nation
        
        new_nation.used_production+=3
        new_nation.used_capital+=150000000
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
            self.owner_nation.oil_raw+=3
            self.owner_nation.resources_produced+=3
        else:
            print(f"Asset {self.uid} is unhooked ")

import nation