import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.mast.label import label
from sbs_utils.procedural import space_objects
from sbs_utils.procedural import roles
from sbs_utils.procedural import routes
from sbs_utils.procedural.execution import jump, AWAIT, get_variable, END
from sbs_utils.procedural.timers import delay_sim
from .simple_common import CommonStory


class Story(CommonStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_text = "This is a start project for mast"
        routes.route_spawn(self.route_ai)

    

    @label()    
    def route_ai(self):
        #
        # SPAWNED_ID is a special value of the ID of the thing spawned
        #
        SPAWNED_ID = get_variable("SPAWNED_ID")
        if roles.has_role(get_variable("SPAWNED_ID"), "raider"):
            print(f"{self.npc_targeting_ai}")
            yield jump(self.npc_targeting_ai)
        #
        # Added others
        #
        # Otherwise, task ends
        yield END()

    @label()    
    def npc_targeting_ai(self):
        SPAWNED_ID = get_variable("SPAWNED_ID")
        the_target = space_objects.closest(SPAWNED_ID, roles.role("__PLAYER__"), 2000)
        if the_target is None:
            the_target = space_objects.closest(SPAWNED_ID, roles.role("Station"))
        if the_target is not None:
            space_objects.target(SPAWNED_ID, the_target, True)

        yield AWAIT(delay_sim(5))
        yield jump(self.npc_targeting_ai)

    