import sbslibs
from  sbs_utils.handlerhooks import *
from sbs_utils.gui import Gui
from sbs_utils.pymast.pymaststorypage import PyMastStoryPage
from sbs_utils.mast.mast import Mast
from story import Story

class SimpleAiPage(PyMastStoryPage):
    story = Story()

Mast.include_code = True

Gui.server_start_page_class(SimpleAiPage)
Gui.client_start_page_class(SimpleAiPage)
