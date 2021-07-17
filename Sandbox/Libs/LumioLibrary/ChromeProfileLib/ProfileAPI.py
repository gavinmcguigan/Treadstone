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
from collections import deque
from threading import Thread 

PROFILE_FOLDER = path.dirname(path.realpath(__file__))
URL_ENDPOINT = 'http://10.7.70.27:5002'

LAST_RECORDED_LOG = deque()
T = None 

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
    def wrapper(email):
        return func(ProfileHandler(email))
    return wrapper 


class ProfileHandler:
    def __init__(self, email):
        self.email_account = email
        self.machine_name = node().replace('-', '').replace('.', '')
        self.zip_filename = f"{email.split('@')[0].replace('.', '')}_{self.machine_name}.zip"
        self.zip_file_location = path.join(PROFILE_FOLDER, self.zip_filename)
        self.profile_folder_location = self.zip_file_location[:-4]
    
    def get_zip_file(self):
        """ 
         1. If profile already present, don't try to download it. 
         2. GET zip file from API Host. 
         3. Unzip to folder
         4. Delete zip file. 
        """

        if path.exists(self.profile_folder_location):
            logger.console(f'Profile {self.profile_folder_location} already exists.')
            return 

        starttime = time()
        r, _ = get(url=f"{URL_ENDPOINT}/profile", timeout=(300, 600), stream=True, 
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
        logger.console(f'\nDownloading chrome profile for account: {self.email_account}')
        self.get_profile_db_entry()
        self.get_zip_file()
        return self.get_webdriver_options()

    def get_webdriver_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-data-dir={self.profile_folder_location}")
        options.add_experimental_option('prefs', {'profile': {'exit_type': 'Normal'}})

        d = DesiredCapabilities.CHROME 
        d['goog:loggingPrefs'] = {'browser': 'ALL'}

        return options, d 


# ------------------------------------  webdriver  ------------------------------------
def get_lib_instance():
    try:
        lib_inst = BuiltIn().get_library_instance('Selenium2Library')
    except:
        raise RuntimeError('No selenium 2 library instance found.')
    else:
        return lib_inst

def get_browser_log(timeout):
    global T 
    while True:
        try:  
            obj = get_lib_instance()
        except RuntimeError:
            sleep(2)
        else:
            driver = obj._current_browser()
            break 

    start = time()
    while time() - start < timeout:
        for entry in driver.get_log('browser'):
            msg = entry.get('message', '')
            indx = msg.find('"')

            LAST_RECORDED_LOG.appendleft(msg[indx+1:-1])

    T = None

def check_for_event_in_console_log(e):
    while True:
        sleep(1)
        if not T:
            break 

    for event in LAST_RECORDED_LOG:
        if e in event:
            logger.console(f"{event} - Found")
        else:
            logger.console(f"{event}")
        logger.console(f"---")


def start_recording_the_console(timeout=60):
    global T
    if not T:
        T = Thread(target=get_browser_log, args=(timeout,), daemon=True)
        T.start()


def find_elements(list_of_elements, timeout=60, retry=2):
    list_of_elements = list_of_elements if isinstance(list_of_elements, list) else [list_of_elements]
    lib_inst = get_lib_instance()
    starttime = time()
    
    while time() - starttime < timeout:
        for n, element in enumerate(list_of_elements):
            try: 
                el = lib_inst.find_element(element)
            except:
                sleep(retry)
            else:
                sleep(1)
                return n, el, element

    raise NoSuchElementException(f'None of the elements passed were found. {str(list_of_elements)}')

# ------------------------------------  Keywords  ------------------------------------
@_profile_handler_inst
def download_chrome_profile(ph):
    """ 
     Takes 1 Argument:  Email address. 
     Attempts to download the chrome profile for passed in email address. 
     Always returns a webdriver.ChromeOptions() instance.    
    """
    return ph.download_chrome_profile()                         

@_profile_handler_inst
def upload_chrome_profile(ph):
    """
     Takes 1 Argument:  Email address. 
     Posts the local profile to the flask server.  
     Returns True if successful else False. 
    """
    return ph.upload_chrome_profile()                           

def upload_chrome_profiles(list_of_emails: list):
    if not isinstance(list_of_emails, list):
        raise ValueError(f"You're attempting to upload more than one chrome profile but you are not passing a list of accounts!")
    results = []
    for email in list_of_emails:
        results.append(upload_chrome_profile(email))
    logger.info(f'Results: {str(results)}')

@_profile_handler_inst
def delete_chrome_profile_from_server(ph):                      
    """
     Takes 1 Argument:  Email address. 
     Delete db entry + the profile zip file on the flask server. 
     Returns True if successful else False.
    """
    return ph.delete_chrome_profile()                           

@_profile_handler_inst
def remove_local_profile(ph):
    """
     Takes 1 Argument:  Email address. 
     Deletes the chrome profile folder + zip file from the local machine if they exist. 
    """
    ph.remove_local_profile()

def get_all_profile_accounts():
    return [a.get('account_email') for a in get(url=f"{URL_ENDPOINT}/emails")[1].get('Emails', [])]    
    
def profile_login_old(email, user_password, url, el="//img[@class='profile-picture']"):
    """
        Takens in 3 Arguments: email account, url, element to look for (optional: default is user profile icon at library).
        Get selenium instance already running via robot.
        Go to the url passed in.
        Look for element passed in. 
            If presented with the welcome back screen, it will go through the 
            flow to login. Eventually, it should get to the url passed in. 
    """
    logger.console(f'Go to: {url}')
    lib_inst = get_lib_instance()
    lib_inst.go_to(url)

    teacher_sign_in_btn = "//button[contains(text(), 'Teacher sign in')]"
    sign_in_with_google = "//*[contains(text(), 'Sign in with Google')]"
    welcome_back_account_button = f"//span[contains(text(), '{email}')]"
    select_google_account = f"//div[contains(@data-identifier, '{email}')]"
    sign_in_with_different_account = f"//input[(@id='sso_signin_skip')]"        # //input[(@value='Sign in with a different account')]
    use_another_account = f"//div[contains(text(), 'Use another account')]"
    email_input = f"//input[(@id='identifierId')]"
    next_button = f"//span[contains(text(),'Next')]"
    password_field = f"//input[(@name='password')]"

    logger.info(f'Trying to login:  Searching for element: {el}')

    # Teacher sign in button OR el=library
    n, element, element_str = find_elements([el, teacher_sign_in_btn])
    
    if n == 1:
        logger.info(f'Found: {element_str}. Clicking.')
        element.click() # Click sign-in button
        
        # Welcome back - Press the button that includes the email OR sign in with google OR sign-in-with-a-different-account
        n, element, element_str = find_elements([welcome_back_account_button, sign_in_with_google, sign_in_with_different_account])
        logger.info(f'Found: {element_str}. Clicking.')
        element.click()

        # If clicked on sign_in_with_different_user
        if n == 2:
            n, element, element_str = find_elements([sign_in_with_google])
            element.click()

        # Select the google account, use another account OR the library
        n, element, element_str = find_elements([select_google_account, use_another_account, el], timeout=30)
        logger.info(f'Found: {element_str}')
        
        if n == 0:
            element.click()
            _, _, element_str = find_elements(el, timeout=30)
    
        elif n == 1:
            # Click on user another account
            element.click()
            _, element = find_elements(email_input, timeout=30)
            # clear email field and enter the email.
            element.clear()
            element.send_keys(f"{email}")
            
            # Locate next button and click it. 
            _, element, _ = find_elements([next_button])
            element.click()

            # Enter password and click next 
            _, element, _ = find_elements([password_field])
            element.clear()
            element.sendKeys(f"{user_password}")

            # Locate next button and click it. 
            _, element, _ = find_elements([next_button])
            element.click()



    logger.info(f'Found: {element_str}')
    sleep(2)

def profile_login_teacher(email, user_password, url, el="//img[@class='profile-picture']"):
    logger.console(f'\n\n')
    logger.console(f'Go to: {url}')
    lib_inst = get_lib_instance()
    lib_inst.go_to(url)
    sleep(5)

    teacher_sign_in_btn = "//button[contains(text(), 'Teacher sign in')]"
    sign_in_with_google = "//*[contains(text(), 'Sign in with Google')]"
    welcome_back_account_button = f"//span[contains(text(), '{email}')]"
    select_google_account = f"//div[contains(@data-identifier, '{email}')]"
    sign_in_with_different_account = f"//input[(@id='sso_signin_skip')]"        # //input[(@value='Sign in with a different account')]
    use_another_account = f"//div[contains(text(), 'Use another account')]"
    email_input = f"//input[(@id='identifierId')]"
    next_button = f"//span[contains(text(),'Next')]"
    password_field = f"//input[(@name='password')]"

    logger.console(f'Trying to login:  target element: {el}')

    # Teacher Sign In Button OR Goes Straight to Lumio Library OR Url passed in.
    n, element, element_str = find_elements([el, teacher_sign_in_btn])
    
    if n == 1:
        logger.console(f'Found: {element_str}. Clicking.')        
        element.click() # Click sign-in button
        
        # Welcome back - Press the button that includes the email OR sign in with google OR sign-in-with-a-different-account
        n, element, element_str = find_elements([welcome_back_account_button, sign_in_with_google, sign_in_with_different_account])
        logger.console(f'Found: {element_str}. Clicking.')
        element.click()

        if n == 0:  # Welcome back flow ------------------------------------------------------------------------------------------
            # WORKING for clicking and going straight to the library
            # Still needs checking for when asking for the password. 
            logger.console(f'Welcome back flow - Should go straight to library OR ask for password.')
            n, element, element_str = find_elements([el, select_google_account])
            if n == 1:
                logger.console(f"Found: {element_str}. Clicking")
                element.click()
                n, element, element_str = find_elements([el, password_field])
                if n == 1:
                    logger.console(f'Asking for password - enter it. ')
                    element.clear()
                    element.send_keys(f"{user_password}")
                    _, element, _ = find_elements([next_button])
                    element.click()

                    _, _, _ = find_elements([el])

        if n == 1:  # First time signing in  ------------------------------------------------------------------------------
            logger.console(f'Sign in with google flow.')
            logger.console(f'Look for email field OR select_google_account - enter email then click next.')
            n, element, _ = find_elements([email_input, select_google_account], timeout=30)
            if n == 0: # WORKING!
                element.clear()
                element.send_keys(f"{email}")
                _, element, _ = find_elements([next_button])
                element.click()

                logger.console(f'Look for password field - enter password then click next.')
                _, element, _ = find_elements([password_field])
                element.clear()
                element.send_keys(f"{user_password}")
                _, element, _ = find_elements([next_button])
                element.click()

                _, _, element_str = find_elements([el])

            elif n == 1: # WORKING!
                logger.console(f'Select the google account.')
                element.click()
                n, element, element_str = find_elements([el, password_field])
                if n == 1:
                    logger.console('Asking for password - enter it. ')
                    element.clear()
                    element.send_keys(f"{user_password}")
                    _, element, _ = find_elements([next_button])
                    element.click()

                    _, _, element_str = find_elements([el])



        if n == 2: # Sign in with google flow ------------------------------------------------------------------------------------
            logger.console(f'Sign in with a different account flow. ')
            
            n, element, element_str = find_elements([select_google_account, use_another_account])
            logger.console(f'Found: {element_str}. Clicking.')

            if n == 0:  # Select the google account
                logger.console(f'Select the google account.')
                element.click()
                n, element, element_str = find_elements([el, password_field])
                if n == 1:
                    logger.console('Asking for password - enter it. ')
                    element.clear()
                    element.send_keys(f"{user_password}")
                    _, element, _ = find_elements([next_button])
                    element.click()

                    _, _, element_str = find_elements([el])


            elif n == 1:    # Use another account
                logger.console(f'Sign in with another account.')
                element.click()

                _, element = find_elements([email_input], timeout=30)
                element.clear()
                element.send_keys(f"{email}")
                _, element, _ = find_elements([next_button])
                element.click()
                
                _, element, _ = find_elements([password_field])
                element.clear()
                element.send_keys(f"{user_password}")
                _, element, _ = find_elements([next_button])
                element.click()

                _, _, element_str = find_elements([el])

    logger.console(f'Found: {element_str}')
    sleep(2)

def profile_login_student(email, user_password, url, classcode, el="//img[@class='profile-picture']"):
    pass