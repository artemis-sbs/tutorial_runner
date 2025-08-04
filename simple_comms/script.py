try:
    import sbslibs
    import sbs
    from  sbs_utils.handlerhooks import *
    from sbs_utils.mast.label import label
    from sbs_utils.mast.pollresults import PollResults
    from sbs_utils.procedural import roles
    from sbs_utils.procedural import routes
    from sbs_utils.procedural import comms
    from sbs_utils.procedural.timers import delay_sim
    from sbs_utils.procedural.execution import AWAIT, END, jump, set_variable, get_variable, task_schedule
    from sbs_utils import faces
    from sbs_utils import fs

    # This allows the script to find the common code
    fs.add_to_path(fs.get_mission_dir_filename("../pymast"))

    from simple_common import CommonStory



    class Story(CommonStory):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.start_text = "This is a start project for mast"
            #routes.route_select_comms(handle_comms)
            routes.route_select_grid(damcon_route)


    @routes.RouteCommsSelect
    @label()
    def handle_comms():
        #
        # This label is called for a player ship (COMMS_ORIGIN_ID)
        # and the COMMS_SELECTED_ID ship has not been communicated with
        # this is used to resolve where to START the conversation with the TO ship
        #
        # COMMS_SELECTED_ID is the id of the target
        COMMS_SELECTED_ID = get_variable("COMMS_SELECTED_ID")
        COMMS_ORIGIN_ID = get_variable("COMMS_ORIGIN_ID")
        
        if COMMS_SELECTED_ID == COMMS_ORIGIN_ID:
            # This is the same ship
            yield jump(internal_comms)
        elif roles.has_role(COMMS_SELECTED_ID, 'Station'):
            yield jump(comms_station)
        elif roles.has_role(COMMS_SELECTED_ID, 'raider'):
            yield jump(npc_comms)

        # Anything else has no comms buttons
        # and static as the id
        #comms_info "static"
        yield END()

    #================ internal_comms ==================
    @label()
    def internal_comms():
        #
        # Setup faces for the departments
        #
        set_variable("doctor", faces.random_terran())
        set_variable("biologist", faces.random_terran())
        set_variable("counselor", faces.random_terran())
        set_variable("major", faces.random_terran())
        yield jump(internal_comms_loop)

    # ================ internal_comms_loop ==================
    @label()
    def internal_comms_loop():
        def button_sickbay():
            comms.comms_receive("The crew health is great!", face=get_variable("doctor"), color="blue", title="sickbay")
            yield PollResults.OK_YIELD 

        def button_security():
            comms.comms_receive("All secure", face=get_variable("major"), color="red", title="security")
            yield PollResults.OK_YIELD
        def button_exobiology():
            comms.comms_receive("Testing running, one moment", face=get_variable("biologist"), color="green", title="exobiology")
            yield PollResults.OK_YIELD 
        def button_counselor():
            comms.comms_receive("Something is disturbing the crew", face=get_variable("counselor"), color="cyan", title="counselor")
            yield AWAIT(delay_sim(seconds=2))
            comms.comms_receive("Things feel like they are getting worse", face=get_variable("counselor"), color="cyan", title="counselor")
            yield PollResults.OK_YIELD 
        
        yield AWAIT(comms.comms("",{
            "sickbay": button_sickbay,
            "security": button_security,
            "exobiology": button_exobiology,
            "counselor": button_counselor,
        }))
        print("BURP")
        # loop
        yield jump(internal_comms_loop)

            

    @label()
    def npc_comms():

        def button_hail(story, comms):
            comms.comms_receive("We will destroy you, disgusting Terran scum!")

        def button_surrender(story, comms):
            comms.comms_receive("OK we give up")

        yield AWAIT(comms.comms("",{
            "Hail": button_hail,
            "Surrender": button_surrender
        }))
        # loop
        yield jump(npc_comms)

    def button_hail(story, comms):
        comms.comms_transmit(f"Hello method")
        comms.comms_receive("Yo")

    @label()
    def comms_station():

        def button_hail():
            comms.comms_transmit(f"Hello function")
            comms.comms_receive("Yo")

        def button_hail_data(story, comms, d):
            comms.comms_transmit(f"Hello {d}")
            comms.comms_receive("Yo")


        yield AWAIT(comms.comms("",{
            "Hail-function": button_hail,
            "Hail-method": button_hail,
            "Pass Data": lambda s,c: button_hail_data(s,c, "Artemis")
        }))
        # loop
        yield jump(comms_station)

    # ================ damcon_route ==================
    #@routes.RouteCommsSelect
    def damcon_route(event):
        COMMS_SELECTED_ID = event.selected_id
        COMMS_ORIGIN_ID = event.origin_id
        # COMMS_SELECTED_ID is the id of the target
        if roles.has_role(COMMS_SELECTED_ID, 'flint'):
            yield jump(comms_flintstone)
        elif roles.has_role(COMMS_SELECTED_ID, 'rubble'):
            yield jump(comms_rubble)
        yield END()

    # ================ comms_flintstone ==================
    @label()
    def comms_flintstone():
        def button_hail():
            comms.broadcast(story.client_id, "Yabba Daba Dooo", "orange")
            

        yield AWAIT(comms.comms("",{
            "Hail": button_hail
        }))
        # -> comms_flintstone
        yield jump(comms_flintstone)

    # ================ comms_rubble ==================
    @label()
    def comms_rubble():
        def button_hail():
            comms.broadcast(get_variable("client_id"), "Hey fred .... how you doin fred?", "brown")


        yield AWAIT(comms.comms("", {
            "Hail": button_hail
        }))
        # -> comms_flintstone
        yield jump(comms_rubble)


    from sbs_utils.mast.maststorypage import StoryPage
    class SimplePage(StoryPage):
        story = Story()
        main_server = story.start_server
        main_client = story.start_client

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