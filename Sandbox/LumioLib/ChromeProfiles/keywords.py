from LumioLib.ChromeProfiles.ProfileAPI import _profile_handler_inst, _get_all_profile_accounts
from LumioLib.ChromeProfiles.login_flow import _login_to_lumio
from robot.api import logger

@_profile_handler_inst
def download_chrome_profile(ph):
    """ 
     Args:  email
     Attempts to download the chrome profile for passed in email address. 
     Returns: a webdriver.ChromeOptions() instance.    
    """
    return ph.download_chrome_profile()                         

@_profile_handler_inst
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

@_profile_handler_inst
def delete_chrome_profile_from_server(ph):                      
    """
        Args:  email
        Delete db entry + the profile zip file on the flask server. 
        Returns: True if successful else False.
    """
    return ph.delete_chrome_profile()                           

@_profile_handler_inst
def remove_local_profile(ph):
    """
        Args:  email
        Deletes the chrome profile folder + zip file from the local machine if they exist. 
        Returns: None
    """
    ph.remove_local_profile() 

def get_profile_accounts():
    """
        Args: None 
        Returns: list dictionaries for each chrome profile on the server. 
    """
    return _get_all_profile_accounts(which='All')


def get_list_of_zips_available():
    """
        Args: None
        Returns: list of zip filenames on the server. 
    """
    return _get_all_profile_accounts(which='Zips')


def profile_login_teacher(email, user_password, url):
    """
        Args: email, password, url
        Returns: None
    """
    _login_to_lumio(email, user_password, url)

def profile_login_student(email, user_password, url, class_code):
    """
        Args: email, password, url
        Returns: None
    """
    _login_to_lumio(email, user_password, url, class_code)

@_profile_handler_inst
def open_cp(ph):
    return ph.open_browser_for_profile()


# --------------------------------------------------------------------------------------------------------------------------------------
@_profile_handler_inst
def open_browser_with_chrome_profile(ph):
    """ 
        This is the only keyword that will open the browser (with chrome profile) using the webdriver, rather than using Robot Framework.

        Args: email
        Returns: the browser after going to the url passed in. 
    """
    return ph.open_browser_for_profile() 