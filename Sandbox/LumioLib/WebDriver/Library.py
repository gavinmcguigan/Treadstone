from LumioLibrary import Driver # import get_chrome_profile, check_for_element, multi_process_func_call
from LumioLibrary import Profiles # import get_profiles
from LumioLibrary import Decs
from LumioLibrary import download_profile

import logging 
logger = logging.getLogger(__name__)

# profiles = Profiles.get_profiles(())
profiles = {
    'Australia': {}, 
    'Canada': {}, 
    'UK': {}, 
    'USA': {}
}

def _login_to_library(foldername, env, pause=False):
    url = f"https://suite.smarttech-{env}.com/login"
    element = "//img[@class='profile-picture']"
    browser = Driver.get_chrome_profile(url, foldername)
    
    if pause:
        return browser, foldername 

    if not Driver.check_for_element(browser, element):
        browser.quit()
        return False, foldername

    browser.quit() 
    return True, foldername 

@Decs.assert_profile_results
def multi_process_login(env='dev'):
    return Driver.multi_process_func_call(_login_to_library, profiles, env)

@Decs.assert_profile_results
def single_process_login(env='dev'):
    return [_login_to_library(d, env) for d in profiles]

@Decs.assert_profile_results
def go_to_library(account, env='prod'):
    
    folderpath = download_profile(account)
    if folderpath:

        url = f"https://suite.smarttech-{env}.com/login"
        element = "//img[@class='profile-picture']"
        browser = Driver.get_chrome_profile(url, folderpath)
        # input('> ')
        
        if not Driver.check_for_element(browser, element):
            browser.quit()
            return [(False, folderpath)]

        browser.quit()
        return [(True, folderpath)]

    return [(False, folderpath)] 

def pause_login(env='dev'):
    browsers = [_login_to_library(d, env, pause=True) for d in profiles]
    input('> ')
    for b, _ in browsers:
        b.quit()
    return [(True, a) for _, a in browsers]

if __name__ == "__main__":
    logger.info('Start...')
    # logger.info(pause_login())
    # logger.info(single_process_login())
    # logger.info(multi_process_login())
    for account in ['Australia', 'Canada', 'Student1', 'Teacher', 'UK', 'USA']:
        logger.info(go_to_library(account))