from LumioLib.PurchaseForm.accounts import PURCHASE_DATA, Account_AUS, UserPass, ElementExpected, PurchaseAccounts
from LumioLib.ChromeProfiles.login_flow import _login_to_lumio
from LumioLib.ChromeProfiles.keywords import open_browser_with_chrome_profile 
from time import sleep, time 
from robot.api import logger

def find_element(browser, xpath, name, action, text):
        try: 
            element = browser.find_element_by_xpath(xpath)
        except:
            logger.info(f'Failed to find element -  {xpath} ')
            return 0
        else:
            if action == 'Click':
                element.click()
            elif action == 'EnterText':
                # element.clear()
                for letter in text:
                    element.send_keys(letter)
                    sleep(0.01)
            return 1

def _fill_in_purchase_form(browser):

    elements = [
        ('//*[@id="name"]', 'Name', 'EnterText', 'gavin'),
        ('//*[@id="line1"]', 'Address Line 1', 'EnterText', 'address address1'),
        ('//*[@id="line2"]', 'Address Line 2', 'EnterText', 'address address2'),
        ('//*[@id="city"]', 'City', 'EnterText', 'Montreal'),
        ('//*[@id="postalCode"]', 'Post Code', 'EnterText', 'H2V 4L2'),
    ]

    total = 0
    start = time()
    while True:
        for xpath, name, action, text in elements:
            total += find_element(browser, xpath, name, action, text)
        
        if total == len(elements):
            print(f'All elements found and actioned!')
            break
        
        if time() - start > 60:
            break


    # if 'USA' not in who:        
    #     if not find_element_add_text(f'//*[contains(@value, "CA")]', 'Click'):
    #         return False 
    #     # select from dropdown "//*[@id='address-fieldset']//*[@name='state']"
    
    # if 'UK' not in who:
    #     if not find_element_add_text('//*[@id="address-fieldset"]//*[@name="state"]', 'State'):
    #         return False
    # else:
    #     if not find_element_add_text(f'//option[contains(@value, "{profile[0][5]}")]', 'Click'):
    #         return False 
    
    # Click Calculate Total Button 
    #if not find_element_add_text('//*[contains(text(),"Calculate total") and contains(@class, "calculate sls-blue-btn")]', 'Click'):
    # if not find_element_add_text('//*[contains(text(),"Calculate total") and contains(@class, "touchbutton-container button button sls-blue-btn uk-text-bold calculate sls-blue-btn")]', 'Click'):
    #    return False
    
    # Add Credit card information
    input('wait >   ')

    return True
            
def go_to_purchase_form_and_fill_in(env='dev'):
    try: 
        browser = open_browser_with_chrome_profile(Account_AUS)
        url = f'https://suite.smarttech-{env}.com/login-purchase'
        login_to_lumio(Account_AUS, UserPass, url=url, element_expected=ElementExpected, lib_inst=browser)
        _fill_in_purchase_form(browser)
        
    finally:
        browser.quit()
    


if __name__ == "__main__":
    go_to_purchase_form_and_fill_in()





# def _purchase_form(account, env, pause=False):
#     url = f"https://suite.smarttech-{env}.com/login-purchase"
#     element = '//button[contains(text(), "Calculate total")]'
#     browser = Driver.get_chrome_profile(url, account)
    
#     if not Driver.check_for_element(browser, element):
#         browser.quit()
#         return False, account 
#     sleep(1)
#     if not _fill_in_purchase_form(browser, account):
#         browser.quit()
#         return False, account 

#     if pause:
#         return browser, account 

#     browser.quit() 
#     return True, account 

# @Decs.assert_profile_results
# def multi_process_purchases(env='dev'):
#     return Driver.multi_process_func_call(_purchase_form, profiles, env)

# @Decs.assert_profile_results
# def single_process_purchases(env='dev'):
#     return [_purchase_form(d, env) for d in profiles]

# def pause_purchase(env='dev'):
#     browsers = [_purchase_form(d, env, pause=True) for d in profiles]
#     input('> ')
#     for b, _ in browsers:
#         b.quit()
#     return [(True, a) for _, a in browsers]


