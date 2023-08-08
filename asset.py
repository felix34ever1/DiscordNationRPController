### Asset class, all Asset subclasses are contained within the economy, political or force script. 

class Asset():

    def __init__(self):
        self.uid = -1 # Unique Identifier
        self.name = "" # Name of the asset e.g refinery or bank etc.
        self.type = "" # Wealth, Political or Force
        
        self.owner_nation = None # Will be assigned when it is hooked by the nation.
        self.has_hooked = False

    def hook(self,owner_nation):
        self.owner_nation = owner_nation
        self.has_hooked = True

    def load_asset(self,json_data:dict):
        self.uid = json_data["uid"]
        self.name = json_data["name"]
        self.type = json_data["type"]

    def export_asset(self)->dict:
        json_data = {}
        json_data["uid"] = self.uid
        json_data["name"] = self.name
        json_data["type"] = self.type
        return(json_data)

    def get_uid(self)->int:
        """Returns the Unique Identifier of the asset"""
        return(self.uid)
