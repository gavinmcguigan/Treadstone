from LumioLib.WebDriver import get_lib_instance
# ppythfrom pynput.keyboard import Key, Controller 
from robot.api import logger
import functools
import platform 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


"""
https://confluence.smarttech.com/pages/viewpage.action?pageId=58344691#UXSpecUndo/redo-ShortcutsonEditmode

"""

win_cmds = {
    'duplicate': 'ctrl+d',
    'copy': ((Keys.CONTROL), ('c',), (Keys.CONTROL)), 
    'paste': 'ctrl+v',
    'delete': 'backspace',
    'lock': 'ctrl+l',
    'unlock': 'ctrl+alt+l',
    'group':  'ctrl+g',
    'ungroup': 'ctrl+shift+g',
    'bring_to_front': 'ctrl+uparrow',
    'send_to_back': 'ctrl+downarrow',
    'undo': 'ctrl+z',
    'redo': 'ctrl+shift+z'
}
mac_cmds = {
    'duplicate': 'cmd+d',
    'copy': (Keys.COMMAND, 'c'),
    'paste': (Keys.COMMAND, 'v'),
    'delete': 'backspace',
    'lock': (Keys.COMMAND, 'l'),
    'unlock': 'cmd+option+l',
    'group':  (Keys.COMMAND, 'g'),
    'ungroup': 'cmd+shift+g',
    'bring_to_front': 'cmd+uparrow',
    'send_to_back': 'cmd+downarrow',
    'undo': (Keys.COMMAND, 'z'),
    'redo': 'cmd+shift+z',
    'select_all': (Keys.COMMAND, 'a')}


# Needs more work - Doesn't work well!
def shortcut_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.console(f"\n{func.__name__.replace('_', ' ').title()}")
        d = mac_cmds if 'Darwin' in platform.system() else win_cmds
        cmd = d.get(func.__name__.replace('shortcuts_', ''))
        logger.console(f'Cmd ->  {cmd}\n')

        action = ActionChains(get_lib_instance())
        action.key_down(cmd[0]).perform()
        action.key_down(cmd[1]).perform()
        action.key_up(cmd[0]).perform()
        action.key_up(cmd[1]).perform()
        # ActionChains(driver).send_keys(*cmd).key_up(*cmd).perform()

        result = func(*args, **kwargs)
        return result 
    return wrapper


