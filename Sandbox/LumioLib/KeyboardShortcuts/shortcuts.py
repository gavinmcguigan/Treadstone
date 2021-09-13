from LumioLib.WebDriver import get_lib_instance
# ppythfrom pynput.keyboard import Key, Controller 
from robot.api import logger
import functools
import platform 
import keyboard

"""
https://confluence.smarttech.com/pages/viewpage.action?pageId=58344691#UXSpecUndo/redo-ShortcutsonEditmode

"""

win_cmds = {
    'duplicate': 'ctrl+d',
    'copy': 'ctrl+c',
    'paste': 'ctrl+v',
    'delete': 'backspace',
    'lock': 'ctrl+l',
    'unlock': 'ctrl+alt+l',
    'group':  'ctrl+g',
    'ungroup': 'ctrl+shift+g',
    'bring_to_front': 'ctrl+uparrow',
    'send_to_back': 'ctrl+downarrow',
    'undo': 'ctrl+z',
    'redo': 'ctrl+shift+z',
    'devtools': 'shift+ctrl+j'
}
mac_cmds = {
    'duplicate': 'cmd+d',
    'copy': 'cmd+c',
    'paste': 'cmd+v',
    'delete': 'backspace',
    'lock': 'cmd+l',
    'unlock': 'cmd+ctrl+l',
    'group':  'cmd+g',
    'ungroup': 'cmd+shift+g',
    'bring_to_front': 'cmd+up',
    'send_to_back': 'cmd+down',
    'undo': 'cmd+z',
    'redo': 'cmd+shift+z',
    'select_all': 'cmd+a',
    'devtools': 'option+cmd+j'
    }



def shortcut_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.console(f"\n{func.__name__.replace('_', ' ').title()}")
        d = mac_cmds if 'Darwin' in platform.system() else win_cmds
        cmd = d.get(func.__name__.replace('shortcuts_', ''))
        if cmd:
            logger.console(f'Cmd ->  {cmd}\n')
            keyboard.press_and_release(cmd)
        result = func(*args, **kwargs)
        return result 
    return wrapper
