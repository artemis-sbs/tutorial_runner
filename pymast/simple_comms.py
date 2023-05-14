import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.pymast.pymaststory import PyMastStory
from sbs_utils.pymast.pymasttask import label
from sbs_utils import query
from sbs_utils import faces
from sbs_utils.objects import PlayerShip, Npc
from sbs_utils.gridobject import GridObject


class Story(PyMastStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_text = "This is a start project for mast"
        self.route_comms_select(self.handle_comms)
        self.route_grid_select(self.damcon_route)

    @label()
    def start_server(self):
        #
        # Create the player ship so the clients see it
        # This is a simple script that has one playable ship
        #

        sbs.create_new_sim()
        

        self.artemis =  query.to_id(PlayerShip().spawn(self.sim, 0,0,0, "Artemis", "tsn", "tsn_battle_cruiser"))
        faces.set_face(self.artemis, faces.random_terran())
        sbs.assign_client_to_ship(0,self.artemis)
        

        go1 = GridObject().spawn(self.sim, self.artemis, "fred", "fred", 9,4, 3, "blue", "flint")
        go2 = GridObject().spawn(self.sim, self.artemis, "barney", "barney", 8,4, 3, "green", "rubble")
        faces.set_face(go1.id, faces.random_terran())
        faces.set_face(go2.id, faces.random_terran())


        print(f"start_server {self.start_text}")
        self.gui_section("area:2,20,80,35;")
        self.gui_text(f""" {self.start_text}""")

        yield self.await_gui({
            "Start": self.start
        })
        
    @label()
    def end_game(self):
        # 
        # Check for end game
        #
        # no more players
        
        players = query.role("__PLAYER__")
        if len(players) == 0:
            self.start_text = "You lost"
            sbs.pause_sim()
            yield self.jump(self.start_server)

        #
        # No more enemies
        #
        raiders = query.role("raider")
        if len(raiders) == 0:
            self.start_text = "You Won"
            print(f"end_game {self.start_text}")
            sbs.pause_sim()
            yield self.jump(self.start_server)
            
        yield self.delay(5)
        yield self.jump(self.end_game)

    @label()
    def handle_comms(self):
        #
        # This label is called for a player ship (COMMS_ORIGIN_ID)
        # and the COMMS_SELECTED_ID ship has not been communicated with
        # this is used to resolve where to START the conversation with the TO ship
        #
        # COMMS_SELECTED_ID is the id of the target

        if self.task.COMMS_SELECTED_ID == self.task.COMMS_ORIGIN_ID:
            # This is the same ship
            yield self.jump(self.internal_comms)
        elif query.has_role(self.task.COMMS_SELECTED_ID, 'Station'):
            yield self.jump(self.comms_station)
        elif query.has_role(self.task.COMMS_SELECTED_ID, 'raider'):
            yield self.jump(self.npc_comms)

        # Anything else has no comms buttons
        # and static as the id
        #comms_info "static"

    #================ internal_comms ==================
    @label()
    def internal_comms(self):
        #
        # Setup faces for the departments
        #
        self.task.doctor = faces.random_terran()
        self.task.biologist = faces.random_terran()
        self.task.counselor = faces.random_terran()
        self.task.major = faces.random_terran()
        yield self.jump(self.internal_comms_loop)

    # ================ internal_comms_loop ==================
    @label()
    def internal_comms_loop(self):
        def button_sickbay(story, comms):
            comms.receive("The crew health is great!", face=story.task.doctor, color="blue", title="sickbay")
        def button_security(story, comms):
            comms.receive("All secure", face=story.task.major, color="red", title="security")
        def button_exobiology(story, comms):
            comms.receive("Testing running, one moment", face=story.task.biologist, color="green", title="exobiology")
        def button_counselor(story, comms):
            comms.receive("Something is disturbing the crew", face=story.task.counselor, color="cyan", title="counselor")
            yield story.delay(seconds=2, use_sim=True)
            comms.receive("Things feel like they are getting worse", face=story.task.counselor, color="cyan", title="counselor")
        
        yield self.await_comms({
            "sickbay": button_sickbay,
            "security": button_security,
            "exobiology": button_exobiology,
            "counselor": button_counselor,
        })
        # loop
        yield self.jump(self.internal_comms_loop)

        # #
        #     + "Exobiology" color "green":
        #         receive  "Testing running, one moment" title "Exobiology" face biologist color "green"
        #         # It is best to schedule delayed responses so the comms buttons are not stalled
        #         schedule test_finished
        #     + "counselor" color "cyan":
        #         receive  "Something is disturbing the crew" title "counselor" face counselor color "cyan"
        #         #
        #         # but you can delay comms, There will be no buttons during this delay
        #         #
        #         delay sim 3s
        #         receive  "Things feel like they are getting worse" title "counselor" face counselor color "cyan"
        # end_await
        # -> internal_comms_loop

    @label()
    def npc_comms(self):

        def button_hail(story, comms):
            comms.receive("We will destroy you, disgusting Terran scum!")

        def button_surrender(story, comms):
            comms.receive("OK we give up")

        yield self.await_comms({
            "Hail": button_hail,
            "Surrender": button_surrender
        })
        # loop
        yield self.jump(self.npc_comms)

    @label()
    def comms_station(self):

        def button_hail(story, comms):
            comms.transmit("Hello")
            comms.receive("Yo")

        yield self.await_comms({
            "Hail": button_hail
        })
        # loop
        yield self.jump(self.comms_station)

    # ================ damcon_route ==================
    @label()
    def damcon_route(self):
        # COMMS_SELECTED_ID is the id of the target
        if query.has_role(self.task.COMMS_SELECTED_ID, 'flint'):
            yield self.jump(self.comms_flintstone)
        elif query.has_role(self.task.COMMS_SELECTED_ID, 'rubble'):
            yield self.jump(self.comms_rubble)

    # ================ comms_flintstone ==================
    @label()
    def comms_flintstone(self):
        def button_hail(story, comms):
            comms.broadcast(story.client_id, "Yabba Daba Dooo", "orange")
            

        yield self.await_comms({
            "Hail": button_hail
        })
        # -> comms_flintstone
        yield self.jump(self.comms_flintstone)

    # ================ comms_rubble ==================
    @label()
    def comms_rubble(self):
        def button_hail(story, comms):
            comms.broadcast(story.client_id, "Hey fred .... how you doin fred?", "brown")


        yield self.await_comms({
            "Hail": button_hail
        })
        # -> comms_flintstone
        yield self.jump(self.comms_rubble)



    @label()
    def start(self):
        # Create the world here

        # Create a space station
        ds1 = Npc().spawn(self.sim, 1000,0,1000, "DS1", "tsn, Station", "starbase_command", "behav_station")
        ds2 = Npc().spawn(self.sim, 1000,0,-1000, "DS2", "tsn, Station", "starbase_command", "behav_station")
        faces.set_face(ds1.id, faces.random_terran())
        faces.set_face(ds2.id, faces.random_terran())

        # Create an enemy
        k001 = Npc().spawn(self.sim, -1000,0,1000, "K001", "raider", "kralien_dreadnaught", "behav_npcship")
        faces.set_face(k001.id, faces.random_kralien())

        sbs.resume_sim()
        yield self.jump(self.end_game)


    @label()
    def start_client(self):
        #
        # This handles the change client button to return to the select_console
        #
        # event change_console:
        #     ->select_console
        # end_event
        #
        # Default the console to helm
        #
        self.task.console_select = "helm"
        yield self.jump(self.select_console)

    @label()
    def select_console(self):
        self.gui_section("area:2,20,80,35;")

        self.gui_text("""Select your console""")

        self.gui_section("area: 85,50, 99,90;row-height:200px")
        console_radio = self.gui_radio("helm,weapons, comms,science,engineering", self.task.console_select, True)
        self.gui_row("row-height: 30px;")
        self.gui_blank()
        self.gui_row("row-height: 30px;")
        self.gui_button("accept", self.console_selected)

        def on_message(sim, event):
            if event.sub_tag.startswith(console_radio.tag):
                self.task.console_select = console_radio.value
                return True

        self.await_gui(on_message=on_message)
        
    @label()
    def console_selected(self):
        sbs.assign_client_to_ship(self.task.page.client_id,self.artemis)
        self.gui_console(self.task.console_select)
        self.await_gui()

