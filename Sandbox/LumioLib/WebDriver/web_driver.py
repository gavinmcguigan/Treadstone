
from robot.libraries.BuiltIn import BuiltIn
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import NoSuchElementException
from LumioLib.ChromeProfiles import open_browser_with_chrome_profile
from selenium import webdriver
import traceback, sys
from robot.api import logger
from time import time, sleep


def get_lib_instance():
    libs = ('SeleniumLibrary', 'Selenium2Library')
    for lib in libs:
        try:
            driver = BuiltIn().get_library_instance(f'{lib}')._current_browser()
        except:
            pass
        else:
            logger.info(f'Using: {lib}')
            return driver
    else:
        raise RuntimeError(f'None of these library instances found: {libs}')


def multi_process_func_call(func, profiles, *args, **kwargs):
    with ThreadPoolExecutor(max_workers=len(profiles)) as exe:
        return [t.result() for t in [exe.submit(func, account, *args, **kwargs) for account in profiles]]



def find_element_and_action(list_of_elements, email, password, class_code, lib_inst, timeout=60, retry=0.5):
    starttime = time()
    
    while time() - starttime < timeout:
        for xpath, descriptor, action in list_of_elements:
            
            try: 
                # el = lib_inst.find_element(xpath)
                el = lib_inst.find_element_by_xpath(xpath)
            except Exception:
                sleep(retry)
                # traceback.print_exc(file=sys.stdout)
            else:
                sleep(1)
                logger.info(f'{descriptor}.')  



                if action is None:
                    return False

                elif action == "click":
                    el.click()
                    
                elif action in ["email", "password"]:
                    el.clear()
                    k = email if action == "email" else password
                    el.send_keys(k)
                    find_element_and_action([("//span[contains(text(),'Next')]", "Next Button", "click")], email, password, class_code, lib_inst)
                    sleep(3)
                
                elif action == "class_code":
                    el.clear()
                    el.send_keys(f"{class_code}")

                return True

    raise NoSuchElementException(f'None of the elements expected were found.')


def actioner(element, name, action)