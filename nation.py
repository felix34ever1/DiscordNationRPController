### Nation Class for holding all data on a nation.
import math
from typing import List
from asset import Asset

class Nation():

    def __init__(self):
        
        # Identifier data used to keep track of country
        self.name = ""
        self.player_name = "" # Discord ID
        self.starting_location = "" # Starting continent

        # Spent resources this turn
        self.used_production = 0
        self.used_capital = 0

        # Capital (money)
        self.capital_current = 0
        # Bottom two are used to do calculations
        self.capital_raw = 0
        self.capital = 0

        # Population
        self.urban_population = 0
        self.rural_population = 0

        # Trackers
        self.political_stability = 0
        self.economy_strength = 0
        
        # For Calculations
        self.predicted_political_stability = 50
        self.predicted_economy_strength = 50

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

        # Statistics used for calculations
        self.resources_produced = 0
        self.resources_spent = 0
        self.outgoing_trade = 0
        self.incoming_trade = 0

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

    def import_data_on_create(self,name:str,urb_pop:int,rur_pop:int,wealth:int,political:int,force:int,owner_id:int,location:str):
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

    def economy_prediction(self)->str:
        self.resources_produced = 0
        self.resources_spent = 0
        self.incoming_trade = 0
        self.outgoing_trade = 0

        self.capital_raw = self.capital_current
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

        # Auto Farming
        self.food_raw+=self.rural_population//1000000
        self.resources_produced+=self.rural_population//1000000

        # Production
        self.production_raw += 2+(self.urban_population//10000000)



        for asset in self.assets_wealth:
            asset.production()
        for asset in self.assets_political:
            asset.production()
        for asset in self.assets_force:
            asset.production()

        self.capital = self.capital_raw - self.used_capital
        self.industrial_metals = self.industrial_metals_raw
        self.rare_metals = self.rare_metals_raw
        self.oil = self.oil_raw
        self.natural_gas = self.natural_gas_raw
        self.food = self.food_raw
        self.production = self.production_raw - self.used_production
        self.plastics = self.plastics_raw
        self.electronics = self.electronics_raw
        self.advanced_parts = self.advanced_parts_raw
        self.consumer_products = self.consumer_products_raw
        self.military_products = self.military_products_raw
        self.power = self.power_raw
        

        for asset in self.assets_wealth:
            asset.upkeep()
        for asset in self.assets_political:
            asset.upkeep()
        for asset in self.assets_force:
            asset.upkeep()

        # Food Consumption
        self.food-=(self.rural_population+self.urban_population)//10000000
        
        # Food to consumer goods
        consumer_products_needed = (self.rural_population+self.urban_population)//20000000
        if self.food>0:
            if self.food//4>=consumer_products_needed: # Produce full amount
                self.consumer_products+=consumer_products_needed
                self.food-=4*consumer_products_needed
            else: # Produce as much as possible
                self.consumer_products+=self.food//4
                self.food = self.food%4
        
        # Consumer Goods Consumption
        self.consumer_products-=consumer_products_needed 

        # Power from fossil fuels, gas used before oil as it has no other uses
        power_needed = (self.rural_population+self.urban_population)//5000000
        if self.natural_gas>0:
            if self.natural_gas*4>=power_needed: # If enough natural gas to create all power:
                self.natural_gas -= power_needed//4
                self.power += (power_needed//4)*4
                if power_needed%4!=0:
                    self.natural_gas-=1
                    self.power+=4
                
            else:
                self.power+=self.natural_gas*4
                self.natural_gas = 0
                power_needed-=self.power
        if self.oil>0: # Oil is here because it will only ever be used if natural gas isn't enough to cover all electricity
            if self.oil*3>power_needed: # If enough oil to create all power:
                self.oil -= power_needed//3
                self.power+=(power_needed//3)*3
                if power_needed%3!=0:
                    self.oil-=1
                    self.power+=3
            else:
                self.power+=self.oil*3
                self.oil = 0                        

        # Power Consumption
        self.power-=(self.urban_population+self.rural_population)//5000000

        self.capital+=( 
            (self.resources_spent+self.resources_produced+self.outgoing_trade-self.incoming_trade)*(self.economy_strength*100000) +
            (((self.urban_population*3)+self.rural_population)*(self.political_stability/50))//6
        )
        

        resources_deficit = 0 #calculate stability
        if self.power<0:
            resources_deficit+= 2*self.power
        if self.food<0:
            resources_deficit+= 2*self.food

        if self.consumer_products+resources_deficit<-15:
            self.predicted_political_stability = 0
        else:
            self.predicted_political_stability = int(300*math.log(((self.consumer_products+resources_deficit)/50)+1)+50)
        
        resources_deficit = 0 #calculate economic strength
        if self.power<0:
            resources_deficit+= 2*self.power
        
        if self.consumer_products+resources_deficit<-31:
            self.predicted_economy_strength = 0
        else:
            self.predicted_economy_strength = int(300*math.log(((self.consumer_products+resources_deficit)/100)+1)+50)


        return(self.economic_report())

    def take_turn(self):
        self.economy_prediction()
        # Figures out resources
        self.capital_current = self.capital
        self.used_capital = 0
        self.used_production = 0
        self.political_stability = self.predicted_political_stability
        self.economy_strength = self.predicted_economy_strength
        # Builds any unfinished assets
        for asset in self.assets_wealth:
            asset.build()
        for asset in self.assets_political:
            asset.build()
        for asset in self.assets_force:
            asset.build()

    def import_data(self,json_data:dict): # Takes the data of a json (Now in python dict not anymore json) and loads the data
        """Using json_data, define all the variables of the nation"""
        self.name = json_data["name"]
        self.player_name = json_data["player name"]
        self.starting_location = json_data["starting location"]

        self.capital_current = json_data["capital"]

        self.used_production = json_data["used production"]
        self.used_capital = json_data["used capital"]

        self.urban_population = json_data["urban population"]
        self.rural_population = json_data["rural population"]

        self.political_stability = json_data["political stability"]
        self.economy_strength = json_data["economy strength"]
        
        self.assets_wealth_id = json_data["assets wealth"]
        self.assets_political_id = json_data["assets political"]
        self.assets_force_id = json_data["assets force"]

        self.wealth_number = json_data["wealth number"]
        self.political_number = json_data["political number"]
        self.force_number = json_data["force number"]
    
    def hook_assets(self,asset_list:list[Asset]):
        """Finds all the assets that belong to the Nation and links them into its own list, as well as telling the asset which nation it belongs to"""
        # Wealth Assets
        for id in self.assets_wealth_id:
            for asset in asset_list:
                if asset.get_uid() == id:
                    self.assets_wealth.append(asset) # Adds the asset to its collection
                    asset.hook(self) # Tells the asset which nation it belongs to
                    break
        # Political Assets
        for id in self.assets_political_id:
            for asset in asset_list:
                if asset.get_uid() == id:
                    self.assets_political.append(asset) # Adds the asset to its collection
                    asset.hook(self) # Tells the asset which nation it belongs to
                    break
        # Force Assets
        for id in self.assets_force_id:
            for asset in asset_list:
                if asset.get_uid() == id:
                    self.assets_force.append(asset) # Adds the asset to its collection
                    asset.hook(self) # Tells the asset which nation it belongs to
                    break

    def export_data(self)->dict:
        """Create a set of json exportable data"""
        json_data = {}

        json_data["name"] = self.name
        json_data["player name"] = self.player_name
        json_data["starting location"] = self.starting_location

        json_data["capital"] = self.capital_current

        json_data["used production"] = self.used_production
        json_data["used capital"] = self.used_capital

        json_data["urban population"] = self.urban_population
        json_data["rural population"] = self.rural_population

        json_data["political stability"] = self.political_stability
        json_data["economy strength"] = self.economy_strength
        
        json_data["wealth number"] = self.wealth_number
        json_data["political number"] = self.political_number
        json_data["force number"] = self.force_number
        


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
Wealth:{self.wealth_number}|Political:{self.political_number}|Force:{self.force_number}
Population:{self.urban_population+self.rural_population}
Stability:{self.political_stability}
Economy:{self.economy_strength}
Wealth Assets:{wealth_asset_string}
Political Assets:{political_asset_string}
Force Assets:{force_asset_string}
''')
        return(text)
    
    def economic_report(self)->str:
        money = self.capital
        if abs(money)>=1000000000:
            money=str(money//1000000000)+"B"
        elif abs(money)>1000000:
            money = str(money//1000000)+"M"
        elif abs(money)>1000:
            money = str(money//1000)+"K"
        
        text = (
        f'''

        {self.name}
        **Resource Profit/Deficit:**
        Capital: ${money}
        Ind. Metals: {self.industrial_metals}
        Rare Metals: {self.rare_metals}
        Oil: {self.oil}
        Natural Gas: {self.natural_gas}
        Food: {self.food}
        Production: {self.production}
        Plastic: {self.plastics}
        Electronics: {self.electronics}
        Advanced Parts: {self.advanced_parts}
        Con. Products: {self.consumer_products}
        Mil. Products: {self.military_products}
        Power: {self.power}
        Predicted Stability: {self.predicted_political_stability}
        Predicted Economic Strength: {self.predicted_economy_strength}
''')

        return(text)