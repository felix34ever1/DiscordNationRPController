### Nation Class for holding all data on a nation.
from typing import List
from asset import Asset

class Nation():

    def __init__(self):
        
        # Identifier data used to keep track of country
        self.name = ""
        self.player_name = "" # Discord ID
        self.starting_location = "" # Starting continent

        # Population
        self.urban_population = 0
        self.rural_population = 0

        # Trackers
        self.political_stability = 0
        self.economy_strength = 0

        # Raw resources are the total income of resources before they are used for anything.
        self.industrial_metals_raw = 0
        self.rare_metals_raw = 0
        self.oil_raw = 0
        self.natural_gas_raw = 0
        self.food_raw = 0
        self.production_raw = 0
        self.plastics_raw = 0
        self.electronics_raw = 0
        self.advanced_parts_raw = 0
        self.consumer_products_raw = 0
        self.military_products_raw = 0
        self.power_raw = 0

        # Calculated resources are the amount of resources left after all the necessary amounts are used up.
        self.industrial_metals = 0
        self.rare_metals = 0
        self.oil = 0
        self.natural_gas = 0
        self.food = 0
        self.production = 0
        self.plastics = 0
        self.electronics = 0
        self.advanced_parts = 0
        self.consumer_products = 0
        self.military_products = 0
        self.power = 0

        # Power Numbers
        self.wealth_number: int = 0
        self.political_number: int = 0
        self.force_number: int = 0

        # Asset list is used to store asset objects.
        self.assets_wealth: List[Asset] = []
        self.assets_political: List[Asset] = []
        self.assets_force: List[Asset] = []

        # List used to store asset IDs
        self.assets_wealth_id: list[int] = []     
        self.assets_political_id: list[int] = []
        self.assets_force_id: list[int] = []

    def import_data_on_create(self,name:str,urb_pop:int,rur_pop:int,wealth:int,political:int,force:int,owner_id:int,location):
        self.name = name
        self.starting_location = location
        self.urban_population = urb_pop
        self.rural_population = rur_pop
        self.wealth_number = wealth
        self.political_number = political
        self.force_number = force
        self.player_name = str(owner_id)
        self.political_stability = 50
        self.economy_strength = 50

    def import_data(self,json_data:dict): # Takes the data of a json (Now in python dict not anymore json) and loads the data
        """Using json_data, define all the variables of the nation"""
        self.name = json_data["name"]
        self.player_name = json_data["player name"]
        self.starting_location = json_data["starting location"]

        self.urban_population = json_data["urban population"]
        self.rural_population = json_data["rural population"]

        self.political_stability = json_data["political stability"]
        self.economy_strength = json_data["economy strength"]
        
        self.assets_wealth_id = json_data["assets wealth"]
        self.assets_political_id = json_data["assets political"]
        self.assets_force_id = json_data["assets force"]

        self.wealth_number = json_data["wealth number"]
        self.political_number = json_data["political number"]
        self.wealth_number = json_data["force number"]
    
    def hook_assets(self,asset_list:list[Asset]):
        """Finds all the assets that belong to the Nation and links them into its own list, as well as telling the asset which nation it belongs to"""
        # Wealth Assets
        for id in self.assets_wealth_id:
            for asset in asset_list:
                if asset.get_uid() == id:
                    self.assets_wealth.append(asset) # Adds the asset to its collection
                    asset.hook(self) # Tells the asset which nation it belongs to
        # Political Assets
        for id in self.assets_political_id:
            for asset in asset_list:
                if asset.get_uid() == id:
                    self.assets_political.append(asset) # Adds the asset to its collection
                    asset.hook(self) # Tells the asset which nation it belongs to
        # Force Assets
        for id in self.assets_political_id:
            for asset in asset_list:
                if asset.get_uid() == id:
                    self.assets_political.append(asset) # Adds the asset to its collection
                    asset.hook(self) # Tells the asset which nation it belongs to

    def export_data(self)->dict:
        """Create a set of json exportable data"""
        json_data = {}
        json_data["name"] = self.name
        json_data["player name"] = self.player_name
        json_data["starting location"] = self.starting_location

        json_data["urban population"] = self.urban_population
        json_data["rural population"] = self.rural_population

        json_data["political stability"] = self.political_stability
        json_data["economy strength"] = self.economy_strength
        
        json_data["wealth number"] = self.wealth_number
        json_data["political number"] = self.political_number
        json_data["force number"] = self.wealth_number

        # Empties the id lists and then reupdates them with all the asset ids.
        self.assets_wealth_id = []
        for asset in self.assets_wealth:
            self.assets_wealth_id.append(asset.get_uid())

        self.assets_political_id = []
        for asset in self.assets_political:
            self.assets_political_id.append(asset.get_uid())      

        self.assets_force_id = []
        for asset in self.assets_force:
            self.assets_force_id.append(asset.get_uid())  

        json_data["assets wealth"] = self.assets_wealth_id
        json_data["assets political"] = self.assets_political_id
        json_data["assets force"] = self.assets_force_id
        return(json_data)

    def display(self)->str:
        wealth_asset_string = "|"
        for asset in self.assets_wealth:
            wealth_asset_string+=asset.name+"|"
        political_asset_string = "|"
        for asset in self.assets_political:
            political_asset_string+=asset.name+"|"
        force_asset_string = "|"
        for asset in self.assets_force:
            force_asset_string+=asset.name+"|"
        text = (
f'''
{self.name}
Population:{self.urban_population+self.rural_population}
Stability:{self.political_stability}
Economy:{self.economy_strength}
Wealth Assets:{wealth_asset_string}
Political Assets:{political_asset_string}
Force Assets:{force_asset_string}
''')
        return(text)