import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.mast.maststorypage import StoryPage
from sbs_utils.mast.label import label
from sbs_utils.mast.pollresults import PollResults
from sbs_utils.mast.mast import Mast
from sbs_utils.gui import Gui
from sbs_utils.agent import clear_shared

#import pymast.simple_ai as simple_ai
#import pymast.simple_science as simple_science
#import pymast.simple_comms as simple_comms
#import pymast.simple_gui as simple_gui

from sbs_utils.procedural.gui import gui_reroute_server, gui_row, gui_button, gui, gui_section, gui_text
from sbs_utils.procedural.execution import AWAIT
from sbs_utils import fs

start_text = "$text:This is an A >> \u0041 << This is an ellipsis >> \u007c  << AA ;font:gui-3;"
Mast.include_code = True
mission_name = fs.get_mission_name()

@label()
def start_client():
    gui_section("area:2,20,80,35;")
    gui_text(f"""Waiting for the server to select example mission. MY Glyphs >> \u0130 \u0131 <<""")

    yield AWAIT(gui())
    # It should never go beyond this
    assert(False)


@label()
def start_server():
    yield PollResults.OK_RUN_AGAIN
    gui_section("area:2,20,80,35;")
    gui_text(f""" {start_text}""")
 
    def redirect_gui(page_class):
        
        # Future client connects
        Gui.client_start_page_class(page_class)
        # Redirect existing client
        for id, client in Gui.clients.items():
            if client is not None:
                client.pop()
                Gui.push(id,page_class())
        

    def run_simple_ai():
        sbs.run_next_mission(f"{mission_name}/simple_ai")
        
        
    def run_simple_ai_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_ai.mast"

        redirect_gui(SimplePage)
        #yield PollResults.OK_JUMP


    def run_simple_science():
        sbs.run_next_mission(f"{mission_name}/simple_science")

        
    def run_simple_science_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_science.mast"


        redirect_gui(SimplePage)

    def run_simple_collision_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_collision.mast"
        redirect_gui(SimplePage)

    def run_simple_comms():
        sbs.run_next_mission(f"{mission_name}/simple_comms")

    def run_simple_comms_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_comms.mast"

        redirect_gui(SimplePage)

    def run_simple_comms_modal_mast():
        Mast.include_code = True
        class SimplePage(StoryPage):
            story_file = "mast/simple_comms_modal.mast"

        redirect_gui(SimplePage)

    def run_simple_gui():
        sbs.run_next_mission(f"{mission_name}/simple_gui")

    def run_simple_agent_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_agent.mast"
        redirect_gui(SimplePage)

    def run_simple_gui_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_gui.mast"

        redirect_gui(SimplePage)

    def run_cut_scene_mast():
        class SimplePage(StoryPage):
            story_file = "mast/pirate_cut_scene.mast"
            #story_file = "mast/simple_cut_scene.mast"

        redirect_gui(SimplePage)

    def run_all_your_base():
        class SimplePage(StoryPage):
            story_file = "mast/simple_cut_scene.mast"

        redirect_gui(SimplePage)

    def run_early_access_two():
        class SimplePage(StoryPage):
            story_file = "mast/early_access_two_highlights.mast"

        redirect_gui(SimplePage)

    def run_extend_console_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_extend_console.mast"

        redirect_gui(SimplePage)


    gui_section("area:10,30,45,95;row-height: 35px")
    gui_text("Mast")
    gui_row()
    gui_button("simple ai", on_press=run_simple_ai_mast)
    gui_row()
    gui_button("simple science", on_press=run_simple_science_mast)
    gui_row()
    gui_button("simple collision", on_press=run_simple_collision_mast)
    gui_row()
    gui_button("simple agent", on_press=run_simple_agent_mast)
    gui_row()
    gui_button("simple comms", on_press=run_simple_comms_mast)
    gui_row()
    gui_button("Modal comms", on_press=run_simple_comms_modal_mast)
    gui_row()
    gui_button("simple gui", on_press=run_simple_gui_mast)
    gui_row()
    gui_button("simple cut scene", on_press=run_cut_scene_mast)
    gui_row()
    gui_button("All your base", on_press=run_all_your_base)
    gui_row()
    gui_button("Extend Console", on_press=run_extend_console_mast)
    gui_row()
    gui_button("EA2", on_press=run_early_access_two)
    


    gui_section("area:50,30,85,95;row-height: 35px")
    gui_text("Python Mast")
    gui_row()
    gui_button("simple ai", on_press=run_simple_ai)
    gui_row()
    gui_button("simple Science", on_press=run_simple_science)
    gui_row()
    gui_button("simple Comms", on_press=run_simple_comms)
    gui_row()
    gui_button("simple gui", on_press=run_simple_gui)


    yield AWAIT(gui())
    assert(False)
    
            
