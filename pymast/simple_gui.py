import sbslibs
import sbs
from sbs_utils.handlerhooks import *
from sbs_utils.mast.maststory import MastStory
from sbs_utils.mast.pollresults import PollResults
from sbs_utils.mast.label import label

from sbs_utils import faces
import functools
from sbs_utils.procedural.gui import gui_reroute_server, gui_row, gui_button, gui, gui_section, gui_text
from sbs_utils.procedural.gui import gui_checkbox, gui_face, gui_drop_down, gui_slider, gui_input
from sbs_utils.procedural.execution import jump, AWAIT
from sbs_utils.procedural.timers import delay_app

class Story(MastStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.colors = ["black", "red", "green", "blue",
                       "purple", "cyan", "yellow", "#FF00FE", "gray"]
        self.fonts = ["smallest", "gui-1", "gui-2",
                      "gui-3", "gui-4", "gui-5", "gui-6"]
        
        self.faces = [faces.random_terran(),
                      faces.random_terran_female(),
                      faces.random_terran_male(),
                      faces.random_terran_fluid()]

        self.recruits = [
            "Pat:^^Can helm a ship through the toughest of asteroid belts",
            "Gwen:^^A real sharpshooter",
            "Randle:^^Top notch no nonsense scientist",
            "Steve:^^Just out of Detocs. Barely an engineer"
        ]

    @label()
    def start_server(self):
        yield jump(self.start)

    @label()
    def start(self):
        #
        # Create the player ship so the clients see it
        # This is a simple script that has one playable ship
        #
        gui_section("area:0,5,10,95;row-height:35px;")
        gui_button(f"""text: Text""", jump=self.page_gui_text)
        gui_row()
        gui_button(f"""text:Buttons""", jump=self.page_gui_button)
        gui_row()
        gui_button(f"""text: Checkbox""", jump=self.page_gui_checkbox)
        gui_row()
        gui_button(f"""text: Dropdown""", jump=self.page_gui_drop_down)
        gui_row()
        gui_button(f"""text:Slider""", jump=self.page_gui_slider)
        gui_row()
        gui_button(f"""text: Text input""", jump=self.page_gui_text_input)
        gui_row()
        gui_button(f"""text:Clickable""", jump=self.page_gui_clickable)
        gui_row()
        gui_button(f"""text:Reroute""", jump=self.page_reroute)
        

        gui_section("area:25,20,80,85;")
        gui_text(f""" This is an example of creating GUI items """)
        
        #yield self.await_gui()
        yield AWAIT(gui())
        
    @label()
    def start_client(self):
        yield self.jump(self.start)

    @label()
    def page_gui_text(self):
        gui_section("area:2,20,80,95;")
        gui_text(f"""color:black;text: This is test""")
        for i in range(len(self.fonts)):
            gui_row()
            gui_text(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: This is test""")

        # yield self.await_gui({
        #     "menu": self.start
        # })
        g = gui()
        while not g.done():
            yield PollResults.OK_RUN_AGAIN

    @label()
    def page_gui_button(self):
        gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            gui_row()
            gui_button(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: This is test""", None)

        yield self.await_gui({
            "menu": self.start
        })

    @label()
    def page_gui_checkbox(self):
        gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            gui_row()
            gui_checkbox(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: This is test""", i % 2)

        yield self.await_gui({
            "menu": self.start
        })

    @label()
    def page_gui_drop_down(self):
        gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            gui_row()
            gui_drop_down(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: Test;list:Fred,Wilma,Barney,Wilma""")

        yield self.await_gui({
            "menu": self.start
        })

    @label()
    def page_gui_slider(self):
        gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            gui_row()
            # """,
            gui_slider(
                0.5, f"""color:{self.colors[i]};font:{self.fonts[i]};low:0;high:2; show_number:False""", None, None)

        yield self.await_gui({
            "menu": self.start
        })

    @label()
    def page_gui_text_input(self):
        gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            gui_row()
            # """,
            gui_input(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: text; desc: Description/title""", None, None)

        yield self.await_gui({
            "menu": self.start
        })

    @label()
    def page_gui_clickable(self):
        
        def click(recruit):
            self.recruit = recruit
            self.jump(self.page_show_recruit)

        for x in range(len(self.recruits)):
            gui_section(f"area:{10+x*20},20,{25+x*20},65;", "color:white; text:Recruit!; font:gui-5", functools.partial(click, x))
            gui_face(self.faces[x])
            gui_row()
            gui_text(f"""color:cyan;font:gui-3; text:{self.recruits[x]}""")

        yield self.await_gui({
            "menu": self.start
        })

    @label()
    def page_show_recruit(self):
        gui_section("area:2,20,80,95;")
        gui_face(self.faces[self.recruit])
        gui_text(""" Ready for duty """)

        yield self.await_gui({
            "menu": self.start
        })

    @label()
    def page_reroute(self):
        def do_reroute():
            yield self.reroute_gui_all(self.page_show_reroute)

        gui_section("area:2,20,80,55;")
        gui_text(""" Reroute """)
        gui_row("row-height: 55px;");
        gui_button("do reroute", do_reroute)
        

        yield self.await_gui()

    @label()
    def page_show_reroute(self):
        gui_section("area:2,20,80,95;")
        gui_text(""" rerouted """)

        yield self.await_gui({
            "menu": self.start
        })