import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.pymast.pymaststory import PyMastStory
from sbs_utils.pymast.pymasttask import label
from sbs_utils import query
from sbs_utils.objects import PlayerShip, Npc
from .simple_common import CommonStory


class Story(CommonStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_text = "This is a start project for mast"
        self.route_spawn(self.route_ai)

    @label()    
    def route_ai(self):
        #
        # SPAWNED_ID is a special value of the ID of the thing spawned
        #
        if query.has_role(self.task.SPAWNED_ID, "raider"):
            yield self.jump(self.npc_targeting_ai)
        #
        # Added others
        #
        # Otherwise, task ends


    @label()    
    def npc_targeting_ai(self):
        the_target = query.closest(self.task.SPAWNED_ID, query.role("__PLAYER__"), 2000)
        if the_target is None:
            the_target = query.closest(self.task.SPAWNED_ID, query.role("Station"))
        if the_target is not None:
            query.target(self.sim, self.task.SPAWNED_ID, the_target, True)

        yield self.delay(5)
        yield self.jump(self.npc_targeting_ai)
