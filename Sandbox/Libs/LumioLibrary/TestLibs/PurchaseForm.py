from time import sleep, time 
from SLSOLibrary import Driver # import get_chrome_profile, check_for_element, multi_process_func_call
from SLSOLibrary import Profiles # import get_profiles
from SLSOLibrary import Decs


import logging
logger = logging.getLogger(__name__)

profiles = Profiles.get_profiles(('Australia', 'Canada', 'UK', 'USA'))


def _fill_in_purchase_form(browser, who):
    profile = profiles.get(who)
    def find_element_add_text(xpath, txt):
        try: 
            element = browser.find_element_by_xpath(xpath)
        except:
            logger.info(f'{who} Failed to find element -  {xpath} ')
            return False
        else:
            if txt == 'Click':
                element.click()
            else:
                # element.clear()
                for letter in txt:
                    element.send_keys(letter)
                    sleep(0.01)
            return True

    # Add name
    if not find_element_add_text('//*[@id="name"]', profile[0][1]):
        return False

    if 'USA' not in who:
        if not find_element_add_text(f'//*[contains(@value, "{profile[0][0]}")]', 'Click'):
            return False 
        # select from dropdown "//*[@id='address-fieldset']//*[@name='state']"

    # Add first line
    if not find_element_add_text('//*[@id="line1"]', profile[0][2]):
        return False 
    # Add Second line
    if not find_element_add_text('//*[@id="line2"]', profile[0][3]):
        return False 
    # City
    if not find_element_add_text('//*[@id="city"]', profile[0][4]):
        return False 
    

    if 'UK' not in who:
        if not find_element_add_text('//*[@id="address-fieldset"]//*[@name="state"]', profile[0][5]):
            return False
    # else:
    #     if not find_element_add_text(f'//option[contains(@value, "{profile[0][5]}")]', 'Click'):
    #         return False 
    
    # Zip Code
    if not find_element_add_text('//*[@id="postalCode"]', profile[0][6]):
        return False 
 
    # Click Calculate Total Button 
    if not find_element_add_text('//*[contains(text(),"Calculate total") and contains(@class, "calculate sls-blue-btn")]', 'Click'):
    # if not find_element_add_text('//*[contains(text(),"Calculate total") and contains(@class, "touchbutton-container button button sls-blue-btn uk-text-bold calculate sls-blue-btn")]', 'Click'):
        return False
    
    # Add Credit card information


    return True

def _purchase_form(account, env, pause=False):
    url = f"https://suite.smarttech-{env}.com/login-purchase"
    element = '//button[contains(text(), "Calculate total")]'
    browser = Driver.get_chrome_profile(url, account)
    
    if not Driver.check_for_element(browser, element):
        browser.quit()
        return False, account 
    sleep(1)
    if not _fill_in_purchase_form(browser, account):
        browser.quit()
        return False, account 

    if pause:
        return browser, account 

    browser.quit() 
    return True, account 

@Decs.assert_profile_results
def multi_process_purchases(env='dev'):
    return Driver.multi_process_func_call(_purchase_form, profiles, env)

@Decs.assert_profile_results
def single_process_purchases(env='dev'):
    return [_purchase_form(d, env) for d in profiles]

def pause_purchase(env='dev'):
    browsers = [_purchase_form(d, env, pause=True) for d in profiles]
    input('> ')
    for b, _ in browsers:
        b.quit()
    return [(True, a) for _, a in browsers]
   
if __name__ == "__main__":
    logger.info('Start...')
    logger.info(pause_purchase())
    # logger.info(multi_process_purchases())
    # logger.info(single_process_purchases())


    