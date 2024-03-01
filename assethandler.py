import asset
import nation
from discord.ext import commands
from typing import Dict

def create_asset(new_asset:dict,asset_list:list):
    """ Used for instantiating assets when they are loaded in"""
    
    # Get asset type

    # Wealth
    if new_asset["name"] == "Industrial Processing Plant":
        asset_object = asset.IPP()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Petroleum Plant":
        asset_object = asset.PP()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Consumer Industry":
        asset_object = asset.CI()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Rare Metals Refinery":
        asset_object = asset.RMR()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Synthetic Plastic Plant":
        asset_object = asset.SPP()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Electronics Hub":
        asset_object = asset.EH()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Civilian Development":
        asset_object = asset.CD()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    # Political
    elif new_asset["name"] == "Solar Array":
        asset_object = asset.SA()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Hydrostation Dam":
        asset_object = asset.HD()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Labour Programme":
        asset_object = asset.LP()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Subversive Politics":
        asset_object = asset.SP()
        asset_object.load_asset(new_asset)
        asset_object.asset_list = asset_list
        asset_list.append(asset_object)
    # Force
    elif new_asset["name"] == "Military Industry":
        asset_object = asset.MI()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Manual Extraction Site":
        asset_object = asset.MES()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Manual Oil Extraction Site ":
        asset_object = asset.MOES()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
        


class AssetStore():
    def __init__(self,asset_list:list[asset.Asset],nation_list:list[nation.Nation]) -> None:
        self.asset_list = asset_list
        self.nation_list = nation_list
        self.wealth_assets:Dict[str,function]={"Industrial Processing Plant":asset.IPP,"Petroleum Plant":asset.PP,"Consumer Industry":asset.CI,
                                               "Rare Metals Refinery":asset.RMR,"Synthetic Plastic Plant":asset.SPP,"Electronics Hub":asset.EH}
        self.political_assets:Dict[str,function]={"Solar Array":asset.SA,"Hydrostation Dam":asset.HD,"Labour Programme":asset.LP,"Civilian Development":asset.CD,"Subversive Politics":asset.SP}
        self.force_assets:Dict[str,function]={"Military Industry":asset.MI,
                                              "Manual Extraction Site":asset.MES,"Manual Oil Extraction Site":asset.MOES}
        self.idpointer = -1

    def get_asset_directed(self,asset_name:str,asset_type)->str:
        """Returns if the asset is directed or not"""
        # get the asset function
        if asset_type == "wealth":
            selected_asset = self.wealth_assets[asset_name]
        elif asset_type == "political":
            selected_asset = self.political_assets[asset_name]
        elif asset_type == "force":
            selected_asset = self.force_assets[asset_name]
        # create the asset function based on the type of asset:
        created_asset = selected_asset()
        if isinstance(created_asset,asset.DirectedAsset): # If directed, you must choose a nation too
            return("directed")
        else:
            return("undirected")

    def buy_asset(self,asset_name:str,asset_type:str,nation:nation.Nation)->str:
        """Attempts to create a specific asset for a nation, given the nation has enough resources."""
        
        # get the asset function
        if asset_type == "wealth":
            selected_asset = self.wealth_assets[asset_name]
        elif asset_type == "political":
            selected_asset = self.political_assets[asset_name]
        elif asset_type == "force":
            selected_asset = self.force_assets[asset_name]
        
        # create the asset function based on the type of asset:
        created_asset = selected_asset()
        if isinstance(created_asset,asset.Ability):
            created_asset.asset_list = self.asset_list
        elif isinstance(created_asset,asset.Asset):
            pass

        if created_asset.cost_calculation(nation): # Check if can add to nation
            created_asset.uid = self.idpointer
            created_asset.building_purchase(nation) 
            self.asset_list.append(created_asset)
            self.nextID()
            return(f"Successfully created {created_asset.name}")
        else:
            return(f"Not enough resources to create {created_asset.name}")  
        
    def buy_directed_asset(self,asset_name:str,asset_type:str,owner_nation:nation.Nation,target_nation:nation.Nation)->str:
        """Attempts to create a specific directed asset for a nation, given the nation has enough resources."""
        
        # get the asset function
        if asset_type == "wealth":
            selected_asset = self.wealth_assets[asset_name]
        elif asset_type == "political":
            selected_asset = self.political_assets[asset_name]
        elif asset_type == "force":
            selected_asset = self.force_assets[asset_name]
        
        # create the asset function based on the type of asset:
        created_asset:asset.DirectedAsset = selected_asset()
        if isinstance(created_asset,asset.DirectedAbility):
            created_asset.asset_list = self.asset_list
        elif isinstance(created_asset,asset.Asset):
            pass

        if created_asset.cost_calculation(owner_nation): # Check if can add to nation
            created_asset.uid = self.idpointer
            created_asset.building_purchase(owner_nation,target_nation) 
            self.asset_list.append(created_asset)
            self.nextID()
            return(f"Successfully created {created_asset.name}")
        else:
            return(f"Not enough resources to create {created_asset.name}")  

    def preview_assets(self,asset_type:str,type_tier:int)->str:
        """Return a menu of available items based on predetermined user input"""
        text = ""
        if asset_type == "wealth":
            for asset_name in self.wealth_assets:
                selected_asset:asset.Asset = self.wealth_assets[asset_name]()
                if type_tier >= selected_asset.tier:
                    text+=f"- {asset_name}\n"
            return text
        elif asset_type == "political":
            for asset_name in self.political_assets:
                selected_asset:asset.Asset = self.political_assets[asset_name]()
                if type_tier >= selected_asset.tier:
                    text+=f"- {asset_name}\n"
            return text
        elif asset_type == "force":
            for asset_name in self.force_assets:
                selected_asset:asset.Asset = self.force_assets[asset_name]()
                if type_tier >= selected_asset.tier:
                    text+=f"- {asset_name}\n"
            return text
        return("None specified")

    def nextID(self):
        id_set:set = set()
        for asset in self.asset_list:
            id_set.add(asset.uid)
        for i in range(max(id_set)+2):
            if i not in id_set:
                self.idpointer = i
                break