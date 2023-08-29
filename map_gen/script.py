import sbslibs
from  sbs_utils.handlerhooks import *
from sbs_utils.gui import Gui
from sbs_utils.pymast.pymaststorypage import PyMastStoryPage
from story import Story
from sbs_native import MapGenerator
from sbs_utils.mast.mast import Mast

Mast.globals["MapGenerator"] = MapGenerator

class SimpleAiPage(PyMastStoryPage):
    story = Story()

#
# Uncomment this out to have Mast show the mast code in 
# runtime errors
#
Mast.include_code = True


Gui.server_start_page_class(SimpleAiPage)
Gui.client_start_page_class(SimpleAiPage)
