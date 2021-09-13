from LumioLib.ChromeProfiles.ProfileAPI import profile_handler_inst, get_all_profile_accounts
from LumioLib.ChromeProfiles.login_flow import login_to_lumio
from robot.api import logger

@profile_handler_inst
def download_chrome_profile(ph):
    """ 
     Args:  email
     Attempts to download the chrome profile for passed in email address. 
     Returns: a webdriver.ChromeOptions() instance.    
    """
    return ph.download_chrome_profile()                         

@profile_handler_inst
def upload_chrome_profile(ph):
    """
     Args:  email
     Posts the local profile to the flask server.  
     Returns: True if successful else False. 
    """
    return ph.upload_chrome_profile()                           

def upload_chrome_profiles(list_of_emails: list):
    """
    Args: list of emails
    Posts the local profiles to the flask server.
    Returns: list of boolean results
    """
    if not isinstance(list_of_emails, list):
        raise ValueError(f"You're attempting to upload more than one chrome profile but you are not passing a list of accounts!")
    results = []
    for email in list_of_emails:
        results.append(upload_chrome_profile(email))
    logger.info(f'Results: {str(results)}')

@profile_handler_inst
def delete_chrome_profile_from_server(ph):                      
    """
        Takes 1 argument:  email
        Delete db entry + the profile zip file on the flask server. 
        Returns: True if successful else False.
    """
    return ph.delete_chrome_profile()                           

@profile_handler_inst
def remove_local_profile(ph):
    """
        Args:  email
        Deletes the chrome profile folder + zip file from the local machine if they exist. 
        Returns: None
    """
    ph.remove_local_profile() 

def get_all_profile_emails():
    """
        Args: None 
        Returns: list of emails that have a chrome profiles on the server. 
    """
    return get_all_profile_accounts()

def profile_login_teacher(email, user_password, url):
    """
        Args: email, password, url
        Returns: None
    """
    login_to_lumio(email, user_password, url)

def profile_login_student(email, user_password, url, class_code):
    """
        Args: email, password, url
        Returns: None
    """
    login_to_lumio(email, user_password, url, class_code)

# --------------------------------------------------------------------------------------------------------------------------------------
@profile_handler_inst
def open_browser_with_chrome_profile(ph):
    """ 
        This is the only keyword that will open the browser (with chrome profile) using the webdriver, rather than using Robot Framework.

        Args: email
        Returns: the browser after going to the url passed in. 
    """
    return ph.open_browser_for_profile() 