import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.pymast.pymasttask import label
from sbs_utils.procedural import roles
from .simple_common import CommonStory

class Story(CommonStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_text = "This is a start project for mast"
        self.enemy_count = 4
        self.route_science_select(self.handle_science)

    
    @label()
    def handle_science(self):
        #
        # This label is called for a player ship (COMMS_ORIGIN_ID)
        # and the SCIENCE_SELECTED_ID ship has not been communicated with
        # this is used to resolve where to START the conversation with the TO ship
        #
        # SCIENCE_SELECTED_ID is the id of the target

        if roles.has_roles(self.task.SCIENCE_SELECTED_ID, 'tsn, Station'):
            yield self.jump(self.station_science)
        elif roles.has_role(self.task.SCIENCE_SELECTED_ID, 'raider'):
            yield self.jump(self.npc_science)

    @label()
    def station_science(self):
        def button_scan(story, science):
            return "This is a friendly station"
        
        def button_bio(story, science):
            return "Just a bunch of people"
        
        def button_intel(story, science):
            return "The people seem smart enough"

        yield self.await_science({
            "scan": button_scan,
            "bio": button_bio,
            "itl": button_intel,
        })
        
    

    @label()
    def npc_science(self):
        def button_scan(story, science):
            return "Looks like some bad dudes"
        
        def button_bio(story, science):
            return "Whew can smell travel through space?"
        
        def button_intel(story, science):
            return "The have spaceships, but seem quite dumb"

        yield self.await_science({
            "scan": button_scan,
            "bio": button_bio,
            "itl": button_intel,
        })
        
    
        
