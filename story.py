import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.mast.maststorypage import StoryPage
from sbs_utils.mast.label import label
from sbs_utils.mast.pollresults import PollResults
from sbs_utils.mast.mast import Mast
from sbs_utils.gui import Gui

import pymast.simple_ai as simple_ai
import pymast.simple_science as simple_science
import pymast.simple_comms as simple_comms
import pymast.simple_gui as simple_gui

from sbs_utils.procedural.gui import gui_reroute_server, gui_row, gui_button, gui, gui_section, gui_text
from sbs_utils.procedural.execution import AWAIT


start_text = "This runs example from tutorials"
Mast.include_code = True

@label()
def start_client():
    gui_section("area:2,20,80,35;")
    gui_text(f"""Waiting for the server to select example mission.""")

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
        class SimplePage(StoryPage):
            story = simple_ai.Story()
            main_server = story.start_server
            main_client = story.start_client
        redirect_gui(SimplePage)
        #yield PollResults.OK_JUMP
        
        
    def run_simple_ai_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_ai.mast"

        redirect_gui(SimplePage)
        #yield PollResults.OK_JUMP


    def run_simple_science():
        class SimplePage(StoryPage):
            story = simple_science.Story()
            main_server = story.start_server
            main_client = story.start_client
        redirect_gui(SimplePage)

        
    def run_simple_science_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_science.mast"


        redirect_gui(SimplePage)

    def run_simple_collision_mast():
        class SimplePage(StoryPage):
            story_file = "mast/simple_collision.mast"
        redirect_gui(SimplePage)

    def run_simple_comms():
        class SimplePage(StoryPage):
            story = simple_comms.Story()

        redirect_gui(SimplePage)

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
        class SimplePage(StoryPage):
            story = simple_gui.Story()
            main_server = story.start
            main_client = story.start

        redirect_gui(SimplePage)
        #yield PollResults.OK_JUMP
        

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

    def run_grid_editor_mast():
        class SimplePage(StoryPage):
            story_file = "mast/editor_main.mast"

        redirect_gui(SimplePage)

    def run_scatter_viewer():
        class SimplePage(StoryPage):
            story_file = "mast/scatter_viewer.mast"

        redirect_gui(SimplePage)



    gui_section("area:10,30,45,95;row-height: 35px")
    gui_text("Mast")
    gui_row()
    gui_button("simple ai", on_message=run_simple_ai_mast)
    gui_row()
    gui_button("simple science", on_message=run_simple_science_mast)
    gui_row()
    gui_button("simple collision", on_message=run_simple_collision_mast)
    gui_row()
    gui_button("simple comms", on_message=run_simple_comms_mast)
    gui_row()
    gui_button("Modal comms", on_message=run_simple_comms_modal_mast)
    gui_row()
    gui_button("simple gui", on_message=run_simple_gui_mast)
    gui_row()
    gui_button("simple cut scene", on_message=run_cut_scene_mast)
    gui_row()
    gui_button("All your base", on_message=run_all_your_base)
    gui_row()
    gui_button("Extend Console", on_message=run_extend_console_mast)
    gui_row()
    gui_button("Grid Object Editor", on_message=run_grid_editor_mast)
    gui_row()
    gui_button("Scatter Viewer", on_message=run_scatter_viewer)
    gui_row()
    gui_button("EA2", on_message=run_early_access_two)
    


    gui_section("area:50,30,85,95;row-height: 35px")
    gui_text("Python Mast")
    gui_row()
    gui_button("simple ai", on_message=run_simple_ai)
    gui_row()
    gui_button("simple Science", on_message=run_simple_science)
    gui_row()
    gui_button("simple Comms", on_message=run_simple_comms)
    gui_row()
    gui_button("simple gui", on_message=run_simple_gui)


    yield AWAIT(gui())
    assert(False)
    
            
