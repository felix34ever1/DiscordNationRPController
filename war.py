from nation import Nation

class War:

    def __init__(self) -> None:
        """War class, holds data on all nations fighting in war as well as all the battles that are being held. It also determines 
        which units engage eachother in scenarios such as naval or aerial engagement which are based on search and destroy tactics. 
        """
        self.uid = -1 # Unique identifier
        self.name = "" # Name of the war
        self.aggressor_nation_uids:list[str] = [] # player names used as UID
        self.aggressor_nations:list[Nation] = []
        self.defender_nation_uids:list[str] = [] # Player names used as UID
        self.defender_nations:list[Nation] = []
        self.battles:list[Battle] = []
        self.battle_uids:list[int] = []

    def hook_nations(self,nation_list:list[Nation]):
        for nation in nation_list:
            if nation.player_name in self.aggressor_nation_uids:
                self.aggressor_nations.append(nation)
            elif nation.player_name in self.defender_nation_uids:
                self.defender_nations.append(nation)


    def load_war(self,json_data:dict):
        """ Takes json data in the form of a dictionary and loads its properties from there"""
        self.uid = json_data["uid"]
        self.name = json_data["name"]
        self.aggressor_nation_uids = json_data["aggressor nation uid"]
        self.defender_nation_uids = json_data["defender nation uid"]
        self.battle_uids = json_data["battle uids"]

    def export_war(self)->dict:
        """Turn the asset into json data to be exported, returns a dictionary"""
        json_data = {}
        json_data["uid"] = self.uid
        json_data["name"] = self.name
        json_data["aggressor nation uid"] = self.aggressor_nation_uids
        json_data["defender nation uid"] = self.defender_nation_uids
        json_data["battle uids"] = self.battle_uids

        return(json_data)

class Battle:

    def __init__(self) -> None:
        pass


def nextWarID(war_list:list[War])->int:
    """Finds the next free ID to use for a new War.

    Args:
        war_list (list[War]): List of all wars.

    Returns:
        int: The lowest free ID for a war.
    """
    id_set:set = set()
    for war in war_list:
        id_set.add(war.uid)
    for i in range(max(id_set)+2):
        if i not in id_set:
            return(i)