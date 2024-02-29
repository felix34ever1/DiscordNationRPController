import asset
import nation
from typing import Dict

def create_asset(new_asset:dict,asset_list:list):
    """ Used for instantiating assets when they are loaded in"""
    
    # Get asset type
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
    elif new_asset["name"] == "Solar Array":
        asset_object = asset.SA()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Hydrostation Dam":
        asset_object = asset.HD()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Military Industry":
        asset_object = asset.MI()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)
    elif new_asset["name"] == "Labour Programme":
        asset_object = asset.LP()
        asset_object.load_asset(new_asset)
        asset_list.append(asset_object)


class AssetStore():
    def __init__(self) -> None:
        self.wealth_assets:Dict[str,function]={"Industrial Processing Plant":asset.IPP,"Petroleum Plant":asset.PP,"Commercial Industry":asset.CI}
        self.political_assets:Dict[str,function]={"Solar Array":asset.SA,"Hydrostation Dam":asset.HD,"Labour Programme":asset.LP}
        self.force_assets:Dict[str,function]={"Military Industry":asset.MI}
        self.idpointer = 0

    def buy_asset(self,asset_name:str,asset_type:str,asset_list:list,nation:nation.Nation)->str:
        """Attempts to create a specific asset for a nation, given the nation has enough resources."""
        
        if asset_type == "wealth":
            selected_asset = self.wealth_assets[asset_name]
        elif asset_type == "political":
            selected_asset = self.political_assets[asset_name]
        elif asset_type == "force":
            selected_asset = self.force_assets[asset_name]
        created_asset:asset.Asset = selected_asset()            
        
        if created_asset.cost_calculation(nation): # Check if can add to nation
            created_asset.uid = self.idpointer
            self.idpointer+=1
            created_asset.building_purchase(nation) 
            asset_list.append(created_asset)
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
