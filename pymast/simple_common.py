import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.mast.maststory import MastStory
from sbs_utils.mast.label import label
from sbs_utils.procedural import query, roles, spawn
from sbs_utils.procedural.execution import AWAIT, jump, get_variable, set_variable
from sbs_utils.procedural.timers import delay_sim
from sbs_utils import faces
from sbs_utils.procedural.gui import gui_row, gui_button, gui_blank, gui, gui_section, gui_text, gui_vradio, gui_console


class CommonStory(MastStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_text = "This is a start project for mast"
        self.enemy_count = 1

    @label()
    def start_server(self):
        #
        # Create the player ship so the clients see it
        # This is a simple script that has one playable ship
        #
        sbs.create_new_sim()
        #yield self.delay(1)

        self.artemis =  query.to_id(spawn.player_spawn(0,0,0, "Artemis", "tsn", "tsn_battle_cruiser"))
        faces.set_face(self.artemis, faces.random_terran())
        sbs.assign_client_to_ship(0,self.artemis)

        print(f"start_server {self.start_text}")
        gui_section("area:2,20,80,35;")
        gui_text(f""" {self.start_text}""")

        # gui_choice("Start", label=self.start)
        gui_section("area:2,90,80,95;")
        def go():
            yield jump(self.start)
        gui_button("start", on_press=go)

        yield AWAIT(gui({"start": go}))

        
    @label()
    def end_game(self):
        # 
        # Check for end game
        #
        # no more players
        
        players = roles.role("__PLAYER__")
        if len(players) == 0:
            self.start_text = "You lost"
            sbs.pause_sim()
            yield jump(self.start_server)
        #
        # No more enemies
        #
        raiders = roles.role("raider")
        if len(raiders) == 0:
            self.start_text = "You Won"
            print(f"end_game {self.start_text}")
            sbs.pause_sim()
            yield jump(self.start_server)
            
        yield AWAIT(delay_sim(5))
        print("End game")
        yield jump(self.end_game)

    @label()
    def start(self):
        # Create the world here

        # Create a space station
        ds1 = spawn.npc_spawn(1000,0,1000, "DS1", "tsn, Station", "starbase_command", "behav_station")
        ds2 = spawn.npc_spawn(1000,0,-1000, "DS2", "tsn, Station", "starbase_command", "behav_station")
        faces.set_face(ds1.id, faces.random_terran())
        faces.set_face(ds2.id, faces.random_terran())

        # Create an enemy
        for i in range(self.enemy_count):
            k001 = spawn.npc_spawn(-1000+300*i,0,1000, f"K00{i}", "raider", "kralien_battleship", "behav_npcship")
            faces.set_face(k001.id, faces.random_kralien())

        sbs.resume_sim()
        yield jump(self.end_game)


    @label()
    def start_client(self):
        #
        # This handles the change client button to return to the select_console
        #
        #
        # Default the console to helm
        #
        print("Client Start Basic AI")
        set_variable("console_select",  "helm")
        yield jump(self.select_console)

    @label()
    def select_console(self):
        gui_section("area:2,20,80,35;")

        gui_text("""Select your console""")

        gui_section("area: 85,50, 99,90;row-height:200px")
        #
        #
        #
        console_radio = gui_vradio("helm,weapons, comms,science,engineering", var="console_select")
        #
        #
        #
        gui_row("row-height: 30px;")
        gui_blank()
        gui_row("row-height: 30px;")
        gui_button("accept", jump=self.console_selected)

        
        yield AWAIT(gui())
        
    @label()
    def console_selected(self):
        sbs.assign_client_to_ship(get_variable("client_id"),self.artemis)
        gui_console(get_variable("console_select"))
        yield AWAIT(gui())


