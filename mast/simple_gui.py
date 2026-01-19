from sbs_utils.procedural.gui import gui_row, gui_text,  gui_icon



def test_template(item):
    gui_row("row-height:1px;background:blue;")
    gui_row("row-height:1px;")
    gui_row("row-height: 25px;background: #1575;")
    gui_row("row-height: 1.2em;padding:13px;")
    gui_icon(f"icon_index: {item['icons'][0]};color:white;")
    gui_text(f"$text:{item.get('test')};justify:left;")
    gui_text("$text:other;justify:right;", "padding: 0,0,0,5px;")
    gui_icon(f"icon_index: {item['icons'][1]};color:green;")
    gui_row("row-height:1px;background:green;")
    gui_row("row-height: 5em;")
    gui_text("$text: hkhjh  j hajkhkjfh  j hfhakf J HFHjkfhkjh afja kjh kjh vskh kjf h kh k fa;", "padding: 0,15px,0,3px;")

def test_horz_template(item):
    gui_row("row-height: 4;col-width: 10em;")
    #gui_icon(f"icon_index: {item['icons'][0]};color:white;")
    gui_text(f"$text:{item['test']};justify:left;", "padding: 5px,0,0,0;")
    #gui_row("row-height: 10;")
    #gui_text("$text: hkhjh  j hajkhkjfh  j hfhakf J HFHjkfhkjh afja kjh kjh vskh kjf h kh k fa;", "padding: 0,15px,0,3px;")
