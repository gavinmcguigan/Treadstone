from selenium import webdriver
from time import time, sleep 
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import NoSuchElementException
import logging 
import asyncio 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s.%(msecs)03d:%(levelname)-8s %(name)-25s   %(message)s")
formatter.datefmt = '%H:%M:%S'
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


profiles = ['Australia', 'UK', 'USA', 'Canada']
chrome_driver_location = "//Users//gav//SLSO//chromedriver"
# url = "chrome://version"
default_location = "//Users//gav//SLSO"

concurrent = False 


def _chrome_options(chrome_options, n):
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{9010 + n}")

    return chrome_options

def _launch_profile(url, n, profile):
    logger.debug(f"{n:<5} {profile}") 

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={default_location}//{profile}")
    options.add_argument("--profile_directory=Profile 1")

    # caps = webdriver.DesiredCapabilities.CHROME.copy()
    # caps["debuggerAddress"] = f"127.0.0.1:{38947 + n}"

    browser = webdriver.Chrome(options=options, executable_path=chrome_driver_location)
    browser.get(url)
    return browser  

async def _check_for_element(browser, element, n):
    starttime = time()
    logger.debug(f"{n} Starttime {starttime:<0.2f}")
    while time() - starttime < 30:
        try: 
            browser.find_element_by_xpath(element)
        except NoSuchElementException:
            await asyncio.sleep(0.5)
        else:
            logger.debug(f"{n} Endtime {time() - starttime:<0.2f}")
            return True 
    return False

def login_to_library():
    url = "https://suite.smarttech-dev.com/login?feature=debug,test-mixpanel-tracking"
    element = "//img[@class='profile-picture']"
    return open_url_and_check(url, element) if concurrent else open_and_pause(url, element)
    
def login_to_purchase_form():
    url = "https://suite.smarttech-dev.com/login-purchase"
    element = '//button[contains(text(), "Calculate total")]'
    return open_url_and_check(url, element) if concurrent else open_and_pause(url, element)

def open_url_and_check(url, element_to_check):
    def func(n, who):
        # Clear accounts
        browser = _launch_profile(url, n, who)
        result = _check_for_element(browser, element_to_check)
        browser.quit()
        return result

    with ThreadPoolExecutor(max_workers=4) as exe:
        return [n.result() for n in [exe.submit(func, n, who) for n, who in enumerate(profiles)]]

def open_and_pause(url, element_to_check):
    
    browsers = []
    for n, d in enumerate(profiles):
        browsers.append(_launch_profile(url, n, d))
    
    # userin = input('> ')

    loop = asyncio.get_event_loop()
    coroutines = [_check_for_element(b, element_to_check, n) for n, b in enumerate(browsers)]
    list_of_finished_tasks, _ = loop.run_until_complete(asyncio.wait(coroutines))

    for b in browsers:
        b.quit()

    return [t.result() for t in list_of_finished_tasks]
    

if __name__ == "__main__":
    starttime = time() 
    # logger.debug(login_to_purchase_form())
    logger.debug(login_to_library())
    logger.debug(f"Timetaken: {time() - starttime:0.2f} seconds. ")


    