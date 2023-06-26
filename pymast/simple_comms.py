import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.pymast.pymaststory import PyMastStory
from sbs_utils.pymast.pymasttask import label
from sbs_utils import query
from sbs_utils import faces
from sbs_utils.objects import PlayerShip, Npc
from sbs_utils.gridobject import GridObject
from .simple_common import CommonStory

class Story(CommonStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_text = "This is a start project for mast"
        self.route_comms_select(self.handle_comms)
        self.route_grid_select(self.damcon_route)


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
            yield story.task.delay(seconds=2, use_sim=True)
            comms.receive("Things feel like they are getting worse", face=story.task.counselor, color="cyan", title="counselor")
        
        yield self.await_comms({
            "sickbay": button_sickbay,
            "security": button_security,
            "exobiology": button_exobiology,
            "counselor": button_counselor,
        })
        # loop
        yield self.jump(self.internal_comms_loop)

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



    