import sbslibs
import sbs
from sbs_utils.handlerhooks import *
from sbs_utils.pymast.pymaststory import PyMastStory
from sbs_utils.pymast.pymasttask import label
from sbs_utils import faces
from sbs_utils.objects import PlayerShip, Npc
import functools


class Story(PyMastStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = ["black", "red", "green", "blue",
                       "purple", "cyan", "yellow", "#FF00FE", "gray"]
        self.fonts = ["smallest", "gui-1", "gui-2",
                      "gui-3", "gui-4", "gui-5", "gui-6"]

    @label()
    def start_server(self):
        yield self.jump(self.start)

    @label()
    def start(self):
        #
        # Create the player ship so the clients see it
        # This is a simple script that has one playable ship
        #

        self.gui_section("area:2,20,80,35;")
        self.gui_text(f""" This is an example of creating GUI items """)
        print("I frigin started")
        yield self.await_gui({
            "next": self.page_gui_text
        })

    @label()
    def start_client(self):
        yield self.jump(self.start)

    @label()
    def page_gui_text(self):
        self.gui_section("area:2,20,80,95;")
        self.gui_text(f"""color:black;text: This is test""")
        for i in range(len(self.fonts)):
            self.gui_row()
            self.gui_text(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: This is test""")

        yield self.await_gui({
            "prev": self.start,
            "next": self.page_gui_button
        })

    @label()
    def page_gui_button(self):
        self.gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            self.gui_row()
            self.gui_button(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: This is test""", None)

        yield self.await_gui({
            "prev": self.page_gui_text,
            "next": self.page_gui_checkbox
        })

    @label()
    def page_gui_checkbox(self):
        self.gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            self.gui_row()
            self.gui_checkbox(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: This is test""", i % 2)

        yield self.await_gui({
            "prev": self.page_gui_button,
            "next": self.page_gui_drop_down
        })

    @label()
    def page_gui_drop_down(self):
        self.gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            self.gui_row()
            self.gui_drop_down(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: Test;list:Fred,Wilma,Barney,Wilma""")

        yield self.await_gui({
            "prev": self.page_gui_checkbox,
            "next": self.page_gui_slider
        })

    @label()
    def page_gui_slider(self):
        self.gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            self.gui_row()
            # """,
            self.gui_slider(
                0.5, f"""color:{self.colors[i]};font:{self.fonts[i]};low:0;high:2; show_number:no""", None, None)

        yield self.await_gui({
            "prev": self.page_gui_drop_down,
            "next": self.page_gui_text_input
        })

    @label()
    def page_gui_text_input(self):
        self.gui_section("area:2,20,80,95;")
        for i in range(len(self.fonts)):
            self.gui_row()
            # """,
            self.gui_text_input(
                f"""color:{self.colors[i]};font:{self.fonts[i]};text: text; desc: Description/title""", None, None)

        yield self.await_gui({
            "prev": self.page_gui_drop_down,
            "next": self.page_gui_clickable
        })

    @label()
    def page_gui_clickable(self):
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


        def click(recruit):
            self.recruit = recruit
            self.jump(self.page_show_recruit)

        for x in range(len(self.recruits)):
            self.gui_section(f"area:{10+x*20},20,{25+x*20},65;", "color:white; text:Recruit!; font:gui-5", functools.partial(click, x))
            self.gui_face(self.faces[x])
            self.gui_row()
            self.gui_text(f"""color:cyan;font:gui-3; text:{self.recruits[x]}""")

        yield self.await_gui({
            "prev": self.page_gui_text_input,
            "next": None
        })

    @label()
    def page_show_recruit(self):
        self.gui_section("area:2,20,80,95;")
        self.gui_face(self.faces[self.recruit])
        self.gui_text(""" Ready for duty """)

        yield self.await_gui({
            "prev": self.page_gui_clickable,
            "next": None
        })
