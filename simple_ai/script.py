import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.mast.label import label
from sbs_utils.mast.maststorypage import StoryPage
from sbs_utils.procedural import space_objects
from sbs_utils.procedural import roles
from sbs_utils.procedural import routes
from sbs_utils.procedural.execution import jump, AWAIT, get_variable, END, set_shared_variable, get_shared_variable, task_schedule
from sbs_utils.procedural.timers import delay_sim

# This allows the script to find the common code
sbslibs.add_folder_to_ptython_path("../pymast")
from simple_common import CommonStory



class Story(CommonStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_text = "This is a start project for mast"
        set_shared_variable("script", "basic_ai")
        task_schedule(self.test_await_delay, var="test_task")

    @label()    
    def test_await_delay(self):
        print(f"Test Start")
        yield AWAIT(delay_sim(5))
        print(f"Test Jump")
        yield jump(self.test_await_delay)


   

@routes.RouteSpawn    
def route_ai_py():
    # This is only needed for the nested missions
    if get_shared_variable("script") != "basic_ai":
        return
    #
    # SPAWNED_ID is a special value of the ID of the thing spawned
    #
    SPAWNED_ID = get_variable("SPAWNED_ID")
    if roles.has_role(SPAWNED_ID, "raider"):
        yield jump(npc_targeting_ai_py)
    #
    # Added others
    #
    # Otherwise, task ends
    yield END()



@label()    
def npc_targeting_ai_py():
    SPAWNED_ID = get_variable("SPAWNED_ID")
    the_target = space_objects.closest(SPAWNED_ID, roles.role("__PLAYER__"), 2000)
    if the_target is None:
        the_target = space_objects.closest(SPAWNED_ID, roles.role("Station"))
    if the_target is not None:
        space_objects.target(SPAWNED_ID, the_target, True)

    print(f"NPC Start")
    yield AWAIT(delay_sim(5))
    print(f"NPC Jump")
    yield jump(npc_targeting_ai_py)



class SimplePage(StoryPage):
    story = Story()
    main_server = story.start_server
    main_client = story.start_client
    #redirect_gui(SimplePage)




#Mast.include_code = True

Gui.server_start_page_class(SimplePage)
Gui.client_start_page_class(SimplePage)
