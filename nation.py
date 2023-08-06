### Nation Class for holding all data on a nation.

class Nation():

    def __init__(self):
        
        # Identifier data used to keep track of country
        self.name = ""
        self.player_name = "" # Discord ID
        self.starting_location = "" # Starting continent

        # Population
        self.urban_population = 0
        self.rural_population = 0
        
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

        # Asset list is used to store asset objects.
        self.assets_wealth = []
        self.assets_political = []
        self.assets_force = []     
    
    def import_data(self,json_data:dict):
        """Using json_data, define all the variables of the nation"""
        self.name = json_data["name"]
        self.player_name = json_data["player name"]
        self.starting_location = json_data["starting location"]
        self.urban_population = json_data["urban population"]
        self.rural_population = json_data["rural population"]
        
        self.assets_wealth = json_data["assets wealth"]
        self.assets_political = json_data["assets political"]
        self.assets_force = json_data["assets force"]

    def display(self):
        print(f"{self.name} - Population:{self.urban_population+self.rural_population}")