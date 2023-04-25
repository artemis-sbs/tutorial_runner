import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.pymast.pymaststory import PyMastStory
from sbs_utils.mast.maststoryscheduler import StoryPage
from sbs_utils.pymast.pymaststorypage import PyMastStoryPage
from sbs_utils.pymast.pymasttask import label
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
    def start_server(self):
        #
        # Create the player ship so the clients see it
        # This is a simple script that has one playable ship
        #
        sbs.create_new_sim()
        
        #yield self.delay(1)

        self.artemis =  query.to_id(PlayerShip().spawn(self.sim, 0,0,0, "Artemis", "tsn", "tsn_battle_cruiser"))
        sbs.assign_client_to_ship(0,self.artemis)
        
        self.gui_section("area:2,20,80,35;")
        self.gui_text(f""" {self.start_text}""")

        def run_simple_ai():
            class SimplePage(PyMastStoryPage):
                story = simple_ai.Story()

            Gui.client_start_page_class(SimplePage)
            Gui.push(None, self.task.page.client_id,SimplePage())
            
            
        def run_simple_ai_mast():
            class SimplePage(StoryPage):
                story_file = "mast/simple_ai.mast"

            Gui.client_start_page_class(SimplePage)
            Gui.push(None, self.task.page.client_id, SimplePage())
       

        def run_simple_science():
            class SimplePage(PyMastStoryPage):
                story = simple_science.Story()

            Gui.client_start_page_class(SimplePage)
            Gui.push(None, self.task.page.client_id,SimplePage())

            
        def run_simple_science_mast():
            class SimplePage(StoryPage):
                story_file = "mast/simple_science.mast"

            Gui.client_start_page_class(SimplePage)
            Gui.push(None, self.task.page.client_id, SimplePage())
       
        def run_simple_comms():
            class SimplePage(PyMastStoryPage):
                story = simple_comms.Story()

            Gui.client_start_page_class(SimplePage)
            Gui.push(None, self.task.page.client_id,SimplePage())

        def run_simple_comms_mast():
            class SimplePage(StoryPage):
                story_file = "mast/simple_comms.mast"

            Gui.client_start_page_class(SimplePage)
            Gui.push(None, self.task.page.client_id, SimplePage())
       
        def run_simple_gui():
            class SimplePage(PyMastStoryPage):
                story = simple_gui.Story()

            Gui.client_start_page_class(SimplePage)
            
            page = SimplePage()
            Gui.push(None, self.task.page.client_id, page)
            

        def run_simple_gui_mast():
            class SimplePage(StoryPage):
                story_file = "mast/simple_gui.mast"

            Gui.client_start_page_class(SimplePage)
            page = SimplePage()
            Gui.push(None, self.task.page.client_id, page)
       




        self.gui_section("area:10,30,45,95;row-height: 35px")
        self.gui_text("Mast")
        self.gui_row()
        self.gui_button("simple ai", run_simple_ai_mast)
        self.gui_row()
        self.gui_button("simple science", run_simple_science_mast)
        self.gui_row()
        self.gui_button("simple comms", run_simple_comms_mast)
        self.gui_row()
        self.gui_button("simple gui", run_simple_gui_mast)


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


        yield self.await_gui({
            "Start": self.start
        })
        #print("I'm outy")
        
    