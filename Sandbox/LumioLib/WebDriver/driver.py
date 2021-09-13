from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import NoSuchElementException
from time import time, sleep
import os 

chrome_driver_location = "//Users//gav//Repos//TestRepos//Treadstone//Sandbox//Chrome//Mac_Chromedriver//chromedriver"
default_location = "//Users//gav//Repos//TestRepos//Treadstone//Sandbox//Chrome/Profiles"



def open_chrome_browser(self, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--safebrowsing-disable-extension-blacklist")
    options.add_argument("--safebrowsing-disable-download-protection")
    prefs = {'safebrowsing.enabled': 'true'}
    options.add_experimental_option("prefs", prefs)
    instance = self.create_webdriver('Chrome', desired_capabilities=options.to_capabilities())
    self.go_to(url)

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

def get_chrome_profile(url, profiledir_path):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profiledir_path}")
    options.add_argument("--profile_directory=Profile 1")
    browser = webdriver.Chrome(
        options=options, 
        executable_path=chrome_driver_location) 
        # service_args=["--verbose", f"--log-path={default_location}//{profile}//Profile.log"])        
    browser.get(url)
    return browser 

def check_for_element(browser, element, wait_time=30):
    starttime = time()
    while time() - starttime < wait_time:
        try: 
            browser.find_element_by_xpath(element)
        except NoSuchElementException:
            sleep(0.5)
        else:
            sleep(1)
            return True

    return False  

def multi_process_func_call(func, profiles, *args, **kwargs):
    with ThreadPoolExecutor(max_workers=len(profiles)) as exe:
        return [t.result() for t in [exe.submit(func, account, *args, **kwargs) for account in profiles]]

def open_url(profile_name):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--disable-web-security")
    # default_user_dir = "C:\\Users\\Gavin\\SMART\\TestRepos\\Treadstone\\Sandbox\\Chrome\\Profiles"
    default_user_dir = "C:\\Users\\Gavin\\Desktop\\Profiles"
    profile = os.path.join(default_user_dir, profile_name)
    options.add_argument(f"user-data-dir={profile}")

    browser = webdriver.Chrome(options=options, executable_path="C:\\Users\\Gavin\\SMART\\TestRepos\\Treadstone\\Sandbox\\Chrome\\Win_Chromedrivers\\cd90.exe")      
    browser.get("https://suite.smarttech-prod.com/login")
    
    input("> ")
    browser.quit()


if __name__ == "__main__":    
    open_url("Jessie")
    open_url("Teacher1")
