from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


def open_browser():
    url = f"http://www.google.es/"
    sl = BuiltIn().get_library_instance("Selenium2Library")
    sl.open_browser(url, "chrome")


def get_browser_desired_capabilities():
    logger.info("Getting currently open browser desired capabilities")
    sl = BuiltIn().get_library_instance("SeleniumLibrary")
    return sl.driver.desired_capabilities