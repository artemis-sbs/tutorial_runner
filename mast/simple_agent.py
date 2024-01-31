from sbs_utils.objects import Npc
from sbs_utils.agent import Agent
from sbs_utils.tickdispatcher import TickDispatcher
from sbs_utils.procedural.query import to_object
from sbs_utils.procedural.space_objects import target, closest, clear_target, closest_list
from sbs_utils.procedural.roles import role
from sbs_utils.procedural.science import science_set_scan_data
from sbs_utils import faces
from enum import IntEnum
from random import randint
import sbs
from sbs_utils.procedural.routes import RouteSpawn, RouteDamageObject, RouteCommsSelect, RouteCommsMessage

#
# This may not be the most efficient, but it is the most flexible
#    
def add_resources_to_terrain():
    asteroids = role("__terrain__")
    for asteroid_id in asteroids:
        asteroid = to_object(asteroid_id)
        # this also skips plain asteroids
        if not asteroid.art_id.startswith("asteroid"): # or asteroid.art_id.startswith("nebula"):
            continue 
        
        amount = randint(1000,15000)
        asteroid.set_inventory_value("resource_amount", amount)
        asteroid.add_role("resource_source")
        # ArtID is the the resource Type
        asteroid.add_role(asteroid.art_id)

class HarvesterState(IntEnum):
    UNKNOWN = 0
    EMPTY_WAITING = 1
    EMPTY  = 2
    HARVESTING = 3
    FULL_WAITING = 4
    FULL = 5
    RETURNING = 6
    EMPTYING = 7


class Harvester(Npc):
    def __init__(self):
        super().__init__()

        self.amount = 0
        self.storage = 4000
        self.state = HarvesterState.EMPTY_WAITING
        self.resource_type = None
        self.face_desc = faces.random_terran(civilian=True)

    @RouteSpawn
    def handle_spawn(self):
        pls = role("__player__")
        for pl in pls:
            science_set_scan_data(pl, self.id,  "Scan data")

    @RouteDamageObject
    def handle_damage(self, event):
        #roid_id = event.selected_id
        roid = to_object(event.selected_id)
        if roid is None:
            # not targeting an asteroid
            return

        if self.state != HarvesterState.HARVESTING:
            # not harvesting so skip
            return

        roid_amount = roid.get_inventory_value("resource_amount")
        if roid_amount is None:
            return
        
        if roid_amount < 50:
            self.find_target()
        if self.amount >= self.storage:
            sbs.send_comms_message_to_player_ship(
                0, self.id, self.face_desc, self.comms_id, "green",
                "Cargo hold full!", "white")
            self.state = HarvesterState.FULL_WAITING
            self.find_target()
        else:
            roid_amount -= 50
            roid.set_inventory_value("resource_amount", roid_amount)

            self.amount += 50
            per = 100*(self.amount/self.storage)
            if per % 10 == 0:
                sbs.send_comms_message_to_player_ship(
                    0, self.id, 
                    self.face_desc, self.comms_id, "yellow",
                    f"{per}% filled", "white")
        

    def spawn(self, x,y,z, side):
        ship = super().spawn(x,y,z, None, side,  "tsn_escort", "behav_npcship")
        self.set_name(f"CIV {ship.id &0xfffffff}")
        self.state = HarvesterState.EMPTY_WAITING
        return ship
    
    def find_target(self):
        if self.state == HarvesterState.HARVESTING:
            print(f"looking for {self.resource_type}")

            close = closest(self, role(self.resource_type))
            if close is not None:
                target(self, close)
        elif self.state == HarvesterState.FULL_WAITING:
            clear_target(self)
            #self.comms_selected(sim, 0, None) ## THIS IS THE WRONG PLAYER ID

    
    def think(self, task):
        if self.state == HarvesterState.RETURNING:
            test = sbs.distance_id(self.id, task.base_id)
            if test < 600:
                self.state = HarvesterState.EMPTYING
                # change delay to 2 sec
                task.delay = 2
        elif self.state == HarvesterState.EMPTYING:
            self.amount -= 100
            base = Agent.get(task.base_id)
            if base is not None:
                cur = base.get_inventory_value(f"storage_{self.resource_type}",0)
                base.set_inventory_value(f"storage_{self.resource_type}",cur+100)
                per = 100*(self.amount/self.storage)
                if per % 10 == 0:
                    sbs.send_comms_message_to_player_ship(
                        0, self.id, 
                        self.face_desc, self.comms_id, "green", 
                        f"Emptying {per}% left", "yellow")
            if self.amount <= 0:
                self.state = HarvesterState.EMPTY_WAITING
                task.stop()
                sbs.send_comms_message_to_player_ship(
                    0, self.id, 
                    self.face_desc, self.comms_id, "green",
                    f"Empty",  "white")
                
    @RouteCommsSelect
    def comms_selected(self, player_id, _):
        sbs.send_comms_selection_info(player_id, self.face_desc, "green", self.comms_id)
        
        # if Empty it is waiting for what to harvest
        if self.state == HarvesterState.EMPTY_WAITING:
            sbs.send_comms_button_info(player_id, "blue", "Harvest energy", "get_energy")
            sbs.send_comms_button_info(player_id, "red", "Harvest minerals", "get_mineral")
            sbs.send_comms_button_info(player_id, "gold", "Harvest rare metals", "get_rare")
            sbs.send_comms_button_info(player_id, "silver", "Harvest alloys", "get_alloy")
            sbs.send_comms_button_info(player_id, "green", "Harvest replicator fuel", "get_food")


        if self.state == HarvesterState.FULL_WAITING:
            for base in closest_list(self, role('station')):
                #base = to_object(base_id)
                sbs.send_comms_button_info(player_id, "yellow", f"Head to {base.py_object.comms_id}", f"{base.py_object.id}")

    @RouteCommsMessage
    def comms_message(self, message, player_id, _):

        if message.isnumeric():
            other_id = int(message)
            target(self, other_id, shoot=False)
            # every ten seconds r
            self.tsk = TickDispatcher.do_interval(self.think, 5)
            self.tsk.base_id = other_id
            self.state = HarvesterState.RETURNING
            return

        match message:
            case 'get_energy':
                self.resource_type = "asteroid_crystal_blue"
                self.send_comms('Gathering energy', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target()
            case 'get_mineral':
                self.resource_type = "asteroid_crystal_red"
                self.send_comms('Gathering minerals', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target()
            case 'get_rare':
                self.resource_type = "asteroid_crystal_yellow"
                self.send_comms('Gathering rare metals', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target()
            case 'get_alloy':
                self.resource_type = "asteroid_crystal_silver"
                self.send_comms('Gathering alloys', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target()
            case 'get_food':
                self.resource_type = "asteroid_crystal_green"
                self.send_comms('Gathering replicator fuel', 'green', player_id)
                self.state = HarvesterState.HARVESTING
                self.find_target()
            case '_':
                return

        # Clear buttons?
        sbs.send_comms_selection_info(player_id, self.face_desc, "green", self.comms_id)

    def send_comms(self, message, color='green', player_id=0):
        sbs.send_comms_message_to_player_ship(
                    player_id, self.id,  
                    self.face_desc, self.comms_id, color,
                    message, "white")

def harvester_spawn(x,y,z, side):
    return Harvester().spawn(x,y,z,side)

