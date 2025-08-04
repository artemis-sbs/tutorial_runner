try:
    import sbslibs
    import sbs
    from  sbs_utils.handlerhooks import *
    from sbs_utils.mast.label import label
    from sbs_utils.mast.maststorypage import StoryPage
    from sbs_utils.procedural import space_objects
    from sbs_utils.procedural import roles
    from sbs_utils.procedural import query
    from sbs_utils.procedural import routes
    from sbs_utils.procedural.execution import jump, AWAIT, get_variable, END, set_shared_variable, get_shared_variable, task_schedule
    from sbs_utils.procedural.timers import delay_sim
    from sbs_utils.gui import Gui

    # This allows the script to find the common code
    sbslibs.add_folder_to_ptython_path("../pymast")
    from simple_common import CommonStory

    # from multiprocessing import shared_memory
    # shm_a = shared_memory.SharedMemory(name="art_test", create=True, size=10)



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

    count = 0

    @label()    
    def npc_targeting_ai_py():
        global count
        SPAWNED_ID = get_variable("SPAWNED_ID")
        the_target = space_objects.closest(SPAWNED_ID, roles.role("__PLAYER__"), 2000)
        if the_target is None:
            the_target = space_objects.closest(SPAWNED_ID, roles.role("Station"))
        if the_target is not None:
            space_objects.target(SPAWNED_ID, the_target, True)

        print(f"NPC Start")
        yield AWAIT(delay_sim(1))
        print(f"NPC Jump")
        player = query.to_object(the_target)
        #### OSC data grab
        t = player.data_set.get("playerThrottle", 0)
        t = int(t*50)
        # shm_a.buf[:4] = bytearray([count%255, t,33,44])
        # count += 1
        # if shm_a.buf[6]==1:
        #     pt = shm_a.buf[5]/ 50.0
        #     shm_a.buf[6] = 0
        #     t = player.data_set.set("playerThrottle", pt, 0)
        yield jump(npc_targeting_ai_py)



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