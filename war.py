from nation import Nation
from asset import UnitGroup

class War:

    def __init__(self) -> None:
        """War class, holds data on all nations fighting in war as well as all the fronts that are being held. It also determines 
        which units engage eachother in scenarios such as naval or aerial engagement which are based on search and destroy tactics. 
        """
        self.uid = -1 # Unique identifier
        self.name = "" # Name of the war
        self.aggressor_nation_uids:list[str] = [] # player names used as UID
        self.aggressor_nations:list[Nation] = []
        self.defender_nation_uids:list[str] = [] # Player names used as UID
        self.defender_nations:list[Nation] = []
        self.fronts:list[Front] = []
        self.front_uids:list[int] = []

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
        self.front_uids = json_data["front uids"]

    def export_war(self)->dict:
        """Turn the war into json data to be exported, returns a dictionary"""
        json_data = {}
        json_data["uid"] = self.uid
        json_data["name"] = self.name
        json_data["aggressor nation uid"] = self.aggressor_nation_uids
        json_data["defender nation uid"] = self.defender_nation_uids
        json_data["front uids"] = self.front_uids
    

        return(json_data)

class Front:

    def __init__(self) -> None:
        self.uid = -1
        self.name = ""
        self.battlespace = ""
        self.attacker_unit_group:UnitGroup = None
        self.attacker_unit_group_id = -1
        self.defender_unit_group:UnitGroup = None
        # Alternatively a strategic asset in which case it would target a nation or something, worry about that later tbh, it might be doable through targetable asset instead.
        self.defender_unit_group_id = -1
        self.attack_support_unit_groups:list[UnitGroup] = []
        self.attack_support_unit_group_ids:list[int] = []
        self.defend_support_unit_groups:list[UnitGroup] = []
        self.defend_support_unit_group_ids:list[int] = []
        self.latestlog:str = []
        self.attacker_advantage = 0 # Negative numbers are defender advantage, represents occupation or some shit

    def load_front(self,json_data:dict):
        """ Takes json data in the form of a dictionary and loads its properties from there"""
        self.uid = json_data["uid"]
        self.name = json_data["name"]
        self.battlespace = json_data["battlespace"]
        self.attacker_unit_group_id = json_data["attacker unit group id"]
        self.defender_unit_group_id = json_data["defender unit group id"]
        self.attack_support_unit_group_ids = json_data["attack support unit group ids"]
        self.defend_support_unit_group_ids = json_data["defend support unit group ids"]
        self.latestlog = json_data["latest log"]
        self.attacker_advantage = json_data["attacker advantage"]

    def export_front(self)->dict:
        """Turn the front into json data to be exported, returns a dictionary"""
        json_data = {}
        json_data["uid"] = self.uid
        json_data["name"] = self.name
        json_data["battlespace"] = self.battlespace
        json_data["attacker unit group id"] = self.attacker_unit_group_id
        json_data["defender unit group id"] = self.defender_unit_group_id
        json_data["attack support unit group ids"] = self.attack_support_unit_group_ids
        json_data["defend support unit group ids"] = self.defend_support_unit_group_ids
        json_data["latest log"] = self.latestlog
        json_data["attacker advantage"] = self.attacker_advantage

    def take_turn(self):
        """ Performs combat between the two sides, to be done once per turn, on the take_turn step. """
        with open("lastcombat.log","w") as newlog:
            newlog.close()
        for supportgroup in self.attack_support_unit_groups:
            supportgroup.allied_unit_group = self.attacker_unit_group
            supportgroup.allied_unit_group_id = self.attacker_unit_group_id
            supportgroup.support("lastcombat.log")
        for supportgroup in self.defend_support_unit_groups:
            supportgroup.allied_unit_group = self.defender_unit_group
            supportgroup.allied_unit_group_id = self.defender_unit_group_id
            supportgroup.support("lastcombat.log")
        if self.attacker_unit_group != None:
            self.attacker_unit_group.enemy_unit_group = self.defender_unit_group
            self.attacker_unit_group.attack("lastcombat.log")
        with open("lastcombat.log","r") as latestlog:
            logtext = latestlog.read()
            self.latestlog = logtext
            with open("combat.log","a") as combatlog:
                combatlog.write(logtext)



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