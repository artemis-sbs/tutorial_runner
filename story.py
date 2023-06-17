import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.pymast.pymaststory import PyMastStory
from sbs_utils.mast.maststoryscheduler import StoryPage
from sbs_utils.pymast.pymaststorypage import PyMastStoryPage
from sbs_utils.pymast.pymasttask import label
from sbs_utils.pymast.pollresults import PollResults
from sbs_utils import query
from sbs_utils.objects import PlayerShip, Npc
from sbs_utils.gui import Gui
import pymast.simple_ai as simple_ai
import pymast.simple_science as simple_science
import pymast.simple_comms as simple_comms
import pymast.simple_gui as simple_gui


class Story(PyMastStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_text = "This runs example from tutorials"

    @label()
    def start_client(self):
        self.gui_section("area:2,20,80,35;")
        self.gui_text(f"""Waiting for the server to select example mission.""")
        yield self.await_gui()

    @label()
    def start_server(self):
        self.gui_section("area:2,20,80,35;")
        self.gui_text(f""" {self.start_text}""")

        def redirect_gui(page_class):
            # Redirect server
            Gui.push(None, 0,page_class())
            # Future client connects
            Gui.client_start_page_class(page_class)
            # Redirect existing client
            for id, client in Gui.clients.items():
                if id != 0 and client is not None:
                    client_page = client.page_stack[-1]
                    if client_page:
                        client.page_stack.pop()
                    Gui.push(None, id,page_class())
            

        def run_simple_ai():
            class SimplePage(PyMastStoryPage):
                story = simple_ai.Story()
            redirect_gui(SimplePage)
            yield PollResults.OK_JUMP
            
            
        def run_simple_ai_mast():
            class SimplePage(StoryPage):
                story_file = "mast/simple_ai.mast"

            redirect_gui(SimplePage)
            yield PollResults.OK_JUMP


        def run_simple_science():
            class SimplePage(PyMastStoryPage):
                story = simple_science.Story()

            redirect_gui(SimplePage)

            
        def run_simple_science_mast():
            class SimplePage(StoryPage):
                story_file = "mast/simple_science.mast"

            redirect_gui(SimplePage)

        def run_simple_comms():
            class SimplePage(PyMastStoryPage):
                story = simple_comms.Story()

            redirect_gui(SimplePage)

        def run_simple_comms_mast():
            class SimplePage(StoryPage):
                story_file = "mast/simple_comms.mast"

            redirect_gui(SimplePage)

        def run_simple_comms_modal_mast():
            class SimplePage(StoryPage):
                story_file = "mast/simple_comms_modal.mast"

            redirect_gui(SimplePage)

        def run_simple_gui():
            class SimplePage(PyMastStoryPage):
                story = simple_gui.Story()

            redirect_gui(SimplePage)
            yield PollResults.OK_JUMP
            

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




        self.gui_section("area:10,30,45,95;row-height: 35px")
        self.gui_text("Mast")
        self.gui_row()
        self.gui_button("simple ai", run_simple_ai_mast)
        self.gui_row()
        self.gui_button("simple science", run_simple_science_mast)
        self.gui_row()
        self.gui_button("simple comms", run_simple_comms_mast)
        self.gui_row()
        self.gui_button("Modal comms", run_simple_comms_modal_mast)
        self.gui_row()
        self.gui_button("simple gui", run_simple_gui_mast)
        self.gui_row()
        self.gui_button("simple cut scene", run_cut_scene_mast)
        self.gui_row()
        self.gui_button("All your base", run_all_your_base)


        self.gui_section("area:50,30,85,95;row-height: 35px")
        self.gui_text("PyMast")
        self.gui_row()
        self.gui_button("simple ai", run_simple_ai)
        self.gui_row()
        self.gui_button("simple Science", run_simple_science)
        self.gui_row()
        self.gui_button("simple Comms", run_simple_comms)
        self.gui_row()
        self.gui_button("simple gui", run_simple_gui)


        yield self.await_gui()
            
    