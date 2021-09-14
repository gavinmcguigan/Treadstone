import shutil, zipfile
import requests, functools
from platform import node
from os import path, remove
from time import sleep, time 
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from LumioLib.WebDriver import get_lib_instance

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import BrowserManagementKeywords, browsermanagement
from SeleniumLibrary import SeleniumLibrary


PROFILE_FOLDER = path.join(path.dirname(path.realpath(__file__)), 'Profiles')
URL_ENDPOINT = 'http://10.7.70.27:5002'


def _request_decorator(func):
    @functools.wraps(func)
    def request_decorator_wrapper(*args, **kwargs):      
        kwargs["headers"] = {"User-agent": f"Python-ChromeProfiles-Lib/{requests.__version__}"}
        
        try:
            r = func(*args, **kwargs)
            logger.info(f"{(func.__name__).upper()} -> {kwargs.get('url')}: {r.status_code}")
            js = r.json() if 'application/json' in r.headers.get('content-type') else {}
            # logger.info(f"Json Response: {js}")
        
        except requests.exceptions.Timeout:
            raise Exception(f"Connection Timeout of {kwargs.get('timeout')[0]} secs reached! ")
        
        except requests.exceptions.ConnectionError as ce:
            logger.error(f"{ce}")
            raise Exception(f"Couldn't reach: {kwargs.get('url')}")
        
        except ValueError as ve:
            raise Exception(f"{ve}")

        except KeyboardInterrupt as ki:
            raise Exception(f"{ki}")
        
        else:
            return r, js 

    return request_decorator_wrapper  

@_request_decorator
def post(*args, **kwargs):
    return requests.post(*args, **kwargs)

@_request_decorator
def get(*args, **kwargs):
    return requests.get(*args, **kwargs)

@_request_decorator
def put(*args, **kwargs):
    return requests.get(*args, **kwargs)

@_request_decorator
def delete(*args, **kwargs):
    return requests.delete(*args, **kwargs)

def _profile_handler_inst(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(ProfileHandler(*args, **kwargs))
    return wrapper 

def _get_all_profile_accounts(which):
    # l = [a.get('account_email') for a in get(url=f"{URL_ENDPOINT}/emails")[1].get('Emails', [])]    
    if which == 'All':
        l = get(url=f"{URL_ENDPOINT}/emails")[1].get('Emails', [])
    elif which == 'Zips':
        l = [n.get('zip_filename', None) for n in get(url=f"{URL_ENDPOINT}/emails")[1].get('Emails', [])]

    for e in l:
        logger.info(e)
    return l 

class ProfileHandler(SeleniumLibrary):
    def __init__(self, email):
        self.email_account = email
        self.machine_name = node().replace('-', '').replace('.', '')
        self.zip_filename = f"{email.split('@')[0].replace('.', '')}_{self.machine_name}.zip"
        self.zip_file_location = path.join(PROFILE_FOLDER, self.zip_filename)
        self.profile_folder_location = self.zip_file_location[:-4]
        self.options = None
    
    def get_zip_file(self):
        """ 
         1. If profile already present, don't try to download it. 
         2. GET zip file from API Host. 
         3. Unzip to folder
         4. Delete zip file. 
        """

        if path.exists(self.profile_folder_location):
            logger.console(f'\nChrome profile for {self.email_account} already exists. \n{self.profile_folder_location} ')
            return 

        logger.console(f'\nDownloading chrome profile for account: {self.email_account}')

        starttime = time()
        r, _ = get(url=f"{URL_ENDPOINT}/profile", timeout=(300, 120), stream=True, 
                   params={'email': self.email_account, 'zip_file': self.zip_filename, 'machine_name': self.machine_name})

        if r.status_code == 200:
            total_length = int(r.headers.get('content-length'))
            
            if total_length:
                logger.info(f'Receiving file: {self.zip_filename}')
                with open(self.zip_file_location, 'wb') as f:
                    for data in r.iter_content(chunk_size=4096):
                        f.write(data)

                logger.info(f'File downloaded successfully in {time() - starttime:<0.2f} seconds.  ({total_length/1000/1000:0.2f} Mbs) ')

                with zipfile.ZipFile(f"{self.zip_file_location}", 'r') as zip_ref:
                    zip_ref.extractall(f"{self.profile_folder_location}")
                
                self.delete_file_or_folder(self.zip_file_location)

    def zip_profile(self):
        """ Zip the profile folder"""
        logger.info(f"Zip this folder: {self.profile_folder_location}")
        try:
            if path.exists(self.profile_folder_location):
                self.zip_file_location = shutil.make_archive(f"{self.profile_folder_location}", 'zip', self.profile_folder_location)
                return True
            else:
                logger.info("Folder doesn't exist.")

        except PermissionError as pe:
            logger.error(f"{str(pe)}")

    def get_profile_db_entry(self):
        logger.info(f"GET profile entry for: {self.email_account}\n{100*'-'}")
        r, _ = get(url=f"{URL_ENDPOINT}/email/{self.email_account}", timeout=(5, 5),
                    params={'zip_file': self.zip_filename, 'machine_name': self.machine_name})
        
        if r.status_code == 404:          
            post(url=f"{URL_ENDPOINT}/email/{self.email_account}", 
                 params={'zip_file': self.zip_filename, 'machine_name': self.machine_name})

    def upload_chrome_profile(self):
        logger.console(f'Uploading chrome profile for account: {self.email_account}')
        self.get_profile_db_entry()
        if not self.zip_profile():      # Will fail if the profile doesn't exist. 
            return False

        def file_gen():
            starttime = time()
            total_length = 0

            try:
                with open(self.zip_file_location, 'rb') as zf:
                    while True:
                        bts = zf.read(8*1024)
                        if not bts:
                            break 

                        total_length += len(bts)
                        yield bts

                logger.info(f'File uploaded successfully in {time() - starttime:<0.2f} seconds.  ({total_length/1000/1000:0.2f} Mbs) ')

            except FileNotFoundError as fnfe:
                logger.error(f"{fnfe}")

        r, _ = post(url=f"{URL_ENDPOINT}/profile", timeout=(300, 120), stream=True, data= file_gen(),
               headers={'Content-Type': 'application/octet-stream'},
               params={'email': self.email_account, 'zip_file': self.zip_filename, 'machine_name': self.machine_name}                               
               )
                
        self.delete_file_or_folder(self.zip_file_location)

        return True if r.status_code == 200 else False 

    def delete_file_or_folder(self, which, folder=False):
        try:
            if path.exists(which):
                logger.info(f"Deleting: {which}")
                if folder:
                    shutil.rmtree(which)
                else:
                    remove(which)
            else:
                logger.info(f"Doesn't Exist: {which}")
        except PermissionError as pe:
            logger.error(f"{str(pe)}")
    
    def remove_local_profile(self):
        self.delete_file_or_folder(self.zip_file_location)
        self.delete_file_or_folder(self.profile_folder_location, folder=True)

    def delete_chrome_profile(self):
        """ 
         Delete profile from flask api host, 
         Deletes zip file 
         Deletes db entry. 
        """
        r1, _ = delete(url=f"{URL_ENDPOINT}/profile", timeout=(10, 10), params={'zip_file': self.zip_filename, 'machine_name': self.machine_name})
        r2, _ = delete(url=f"{URL_ENDPOINT}/email/{self.email_account}", timeout=(10, 30), params={'machine_name': self.machine_name})
        
        return True if (r1.status_code == 200 and r2.status_code == 200) else False

    def download_chrome_profile(self):
        self.get_profile_db_entry()
        self.get_zip_file()
        return self.get_webdriver_options()

    def get_webdriver_options(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f"user-data-dir={self.profile_folder_location}")
        self.options.add_experimental_option('prefs', {'profile': {'exit_type': 'Normal'}})
        return self.options

    def open_browser_for_profile(self):
        self.download_chrome_profile()
        print(self.options)
        return webdriver.Chrome(options=self.options)

    def try_this(self):
        self.get_profile_db_entry()
        self.get_zip_file()
        self.get_webdriver_options()

        browser = webdriver.Chrome(options=self.options)
        print(get_lib_instance())
        browser.get('https://www.google.es')
        sleep(10)
        browser.quit()

    # def open_cp_browser(self):
        
    #     self.get_profile_db_entry()
    #     self.get_zip_file()

    #     # options = webdriver.ChromeOptions()
    #     # options.add_argument(f"user-data-dir={self.profile_folder_location}")
    #     # options.add_experimental_option('prefs', {'profile': {'exit_type': 'Normal'}})

        

    #     # print(self.options)
    #     browsermanagement = BrowserManagementKeywords(self)
    #     browsermanagement.open_browser('http://www.google.es', browser='Chrome')

    #     # browsermanagement.create_webdriver('Chrome', options=options)
    #     sleep(10)
    #     # browsermanagement.close_browser()
    #     browsermanagement.close_all_browsers()
    #     #browser_management.open_browser('http://www.google.es', 'chrome')
    #     #self.open_browser('http://www.google.es', 'chrome')

    # def close_cp_browser(self):
    #     self.close_all_browsers()


if __name__ == "__main__":
    inst = ProfileHandler(email='gavinmcguigan.student1@smartwizardschool.com')
    inst.try_this()
    sleep(5)
    #inst.options.close()
    