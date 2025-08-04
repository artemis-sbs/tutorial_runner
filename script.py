try:
    import sbslibs
    from  sbs_utils.handlerhooks import *
    from sbs_utils.gui import Gui
    from sbs_utils.mast.maststorypage import StoryPage
    from sbs_utils.mast.maststory import MastStory

    from sbs_utils.mast.mast import Mast
    from sbs_utils.mast.pollresults import PollResults
    from sbs_utils.mast.label import label
    from story import start_server, start_client

    from sbs_utils.procedural.gui import gui_reroute_server, gui_row, gui_button, gui, gui_section, gui_text


    class Story(MastStory):
        # def __init__(self):
        #     super.__init__()
        #     self.main = self.main_gui

        def test(self):
            print("Press")

        @label()
        def main_gui(self):
            #yield PollResults.OK_RUN_AGAIN
            # gui_reroute_server(server_start)
            gui_section("area: 20,20,50,50")
            gui_button("Hello", on_press=self.test)
            gui_row()
            gui_text("Hello")
            
            g = gui()
            while not g.done():
                yield PollResults.OK_RUN_AGAIN
            


    class SimpleAiPage(StoryPage):
        story = Story()
        main_server = start_server
        main_client = start_client



    Mast.include_code = True

    Gui.server_start_page_class(SimpleAiPage)
    Gui.client_start_page_class(SimpleAiPage)
except Exception as e:
    message = e
    def cosmos_event_handler(sim, event):
        import sbs
        sbs.send_gui_clear(event.client_id, "")
        sbs.send_gui_text(
            event.client_id,"", "text", f"$text:sbs_utils runtime error^{message};", 0, 0, 80, 95)
        sbs.send_gui_complete(event.client_id, "")