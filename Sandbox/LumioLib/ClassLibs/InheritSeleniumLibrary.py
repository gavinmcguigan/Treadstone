from SeleniumLibrary import keywords
from robot.api import logger
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords, browsermanagement
from time import sleep
from selenium import webdriver

from selenium.webdriver.common import desired_capabilities
from LumioLib.WebDriver.keywords import get_lib_instance

class InheritSeleniumLibrary(SeleniumLibrary):
    
    @keyword
    def open_chrome_profile_browser(self):
        browser_management = BrowserManagementKeywords(self)
        options = webdriver.ChromeOptions()
        profile_folder_location = "/Users/gav/Repos/TestRepos/Treadstone/Sandbox/LumioLib/ChromeProfiles/Profiles/gavinmcguiganteacher_GavsMacBookProlocal"
        options.add_argument(f"user-data-dir={profile_folder_location}")
        #options.add_experimental_option('', {'profile': {'exit_type': 'Normal'}})
        brow = browser_management.open_browser(url="chrome://version/", browser="Chrome", desired_capabilities=options.to_capabilities())
        logger.info(brow)
        sleep(3)
        print(get_lib_instance())
        sleep(3)

    @keyword
    def open_browser(self, host):
        browser_management = BrowserManagementKeywords(self)
        b = browser_management.open_browser('chrome://version/', "chrome")
        logger.info(f'{browsermanagement}')
        logger.info(f'{b}')
        return b 


    @keyword
    def get_browser_desired_capabilities(self):
        logger.info("Getting currently open browser desired capabilities")
        return self.driver.desired_capabilities

    def not_keywords_but_public_methods(self):
        logger.info(
            "Python public method not a keyword, because it is not "
            "decorated with @keyword decorator"
        )

    def _private_method_are_not_keywords(self):
        logger.info(
            "Python private method is not a keyword, because it is not "
            "decorated with @keyword decorator"
        )



if __name__ == "__main__":
    inst = InheritSeleniumLibrary()
    inst.open_cp_browser()
    sleep(10)
    inst.close_cp_browser()