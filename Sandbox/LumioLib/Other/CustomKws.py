from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from time import sleep
from selenium.webdriver.common.keys import Keys
import sys



def get_selenium_instance():
    S2L = BuiltIn().get_library_instance('Selenium2Library')
    return S2L 

def s2lext_input_text_controlled(self, locator, text, pause=0.05):
    S2L = get_selenium_instance()

    print("Enter '{}' at locator '{}' with speed {} secs/letter".format(text, locator, pause))
    try:    # robotframework-selenium2library v3.0
        element = S2L.find_element(locator)
    except AttributeError:
        pass
    else:
        element.clear()
        for letter in text:
            element.send_keys(letter)
            sleep(float(pause))
        else:
            # print(help(element))
            return True
    
    return False 

def paste_text(self, locator, text):
    """Pastes the given `text` into text field identified by `locator`.
        Requires that pyperclip be installed on the system  (pip install pyperclip)
    """
    import pyperclip
    S2L = get_selenium_instance()

    pyperclip.copy(text)
    try:    # robotframework-selenium2library v1.8
        element = S2L._element_find(locator, True, True)
    except:
        print("S2L._element_find not supported")
    try:    # robotframework-selenium2library v3.0
        element = S2L.find_element(locator)
    except:
        print("S2L.find_element not supported")
    element.clear()
    

    if 'darwin' in sys.platform:
        # On Mac
        element.send_keys(Keys.COMMAND, 'v')
    else:
        # On Windows
        element.send_keys(Keys.CONTROL, 'v')

    