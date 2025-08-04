try:
    import sbslibs
    import sbs
    from  sbs_utils.handlerhooks import *
    from sbs_utils.mast.label import label
    from sbs_utils.procedural import roles
    from sbs_utils.procedural.execution import jump, AWAIT, get_variable
    from sbs_utils.procedural.science import scan
    from sbs_utils.procedural.routes import RouteScienceSelect
    from sbs_utils.mast.maststorypage import StoryPage


    # This allows the script to find the common code
    sbslibs.add_folder_to_ptython_path("../pymast")
    from simple_common import CommonStory


    class Story(CommonStory):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.start_text = "This is a start project for mast"
            # self.enemy_count = 4
            # route_select_science(self.handle_science)

        
    @RouteScienceSelect
    def handle_science(self):
        #
        # This label is called for a player ship (COMMS_ORIGIN_ID)
        # and the SCIENCE_SELECTED_ID ship has not been communicated with
        # this is used to resolve where to START the conversation with the TO ship
        #
        # SCIENCE_SELECTED_ID is the id of the target
        

        if roles.has_roles(get_variable("SCIENCE_SELECTED_ID"), 'tsn, Station'):
            yield jump(self.station_science)
        elif roles.has_role(get_variable("SCIENCE_SELECTED_ID"), 'raider'):
            yield jump(self.npc_science)

    @label()
    def station_science():
        def button_scan():
            return "This is a friendly station"
        
        def button_bio():
            return "Just a bunch of people"
        
        def button_intel():
            return "The people seem smart enough"
        
        print("Routed science station")

        yield AWAIT(scan({
            "scan": button_scan,
            "bio": button_bio,
            "itl": button_intel,
        }))

        


    @label()
    def npc_science():
        def button_scan():
            return "Looks like some bad dudes"
        
        def button_bio():
            return "Whew can smell travel through space?"
        
        def button_intel():
            return "The have spaceships, but seem quite dumb"
        
        print("Routed science npc")

        yield AWAIT(scan({
            "scan": button_scan,
            "bio": button_bio,
            "itl": button_intel,
        }))
        

        
    class SimplePage(StoryPage):
        story = Story()
        main_server = story.start_server
        main_client = story.start_client
        #redirect_gui(SimplePage)




    #Mast.include_code = True

    Gui.server_start_page_class(SimplePage)
    Gui.client_start_page_class(SimplePage)

except Exception as e:
    message = e
    def cosmos_event_handler(sim, event):
        import sbs
        sbs.send_gui_clear(event.client_id, "")
        sbs.send_gui_text(
            event.client_id,"", "text", f"$text:sbs_utils runtime error^{message};", 0, 0, 80, 95)
        sbs.send_gui_complete(event.client_id, "")
