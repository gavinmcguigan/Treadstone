
from .TestLibs import single_process_purchases
from .TestLibs import multi_process_purchases
from .TestLibs import single_process_login
from .TestLibs import multi_process_login
from .TestLibs import pause_login
from .TestLibs import go_to_library

from .BackendCleanup import stripe_delete_customer_by_email_and_country
from .BackendCleanup import stripe_delete_customer_by_email_and_stripe_account
from .BackendCleanup import stripe_get_customers_on_all_accounts
from .BackendCleanup import stripe_delete_customers_on_all_accounts


from .ChromeProfileLib import download_chrome_profile
from .ChromeProfileLib import upload_chrome_profile
from .ChromeProfileLib import upload_chrome_profiles
from .ChromeProfileLib import delete_chrome_profile_from_server
from .ChromeProfileLib import profile_login_teacher
from .ChromeProfileLib import profile_login_student
from .ChromeProfileLib import remove_local_profile
from .ChromeProfileLib import get_all_profile_accounts
from .ChromeProfileLib import start_recording_the_console
from .ChromeProfileLib import check_for_event_in_console_log

from .Shortcuts import shortcuts_duplicate
from .Shortcuts import shortcuts_copy
from .Shortcuts import shortcuts_paste
from .Shortcuts import shortcuts_delete
from .Shortcuts import shortcuts_lock
from .Shortcuts import shortcuts_unlock 
from .Shortcuts import shortcuts_group 
from .Shortcuts import shortcuts_ungroup
from .Shortcuts import shortcuts_bring_to_front 
from .Shortcuts import shortcuts_bring_to_front 
from .Shortcuts import shortcuts_send_to_back
from .Shortcuts import shortcuts_undo  
from .Shortcuts import shortcuts_redo 
from .Shortcuts import shortcuts_select_all 

# from robot.api import logger
# from robot.libraries.BuiltIn import BuiltIn 

import logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s.%(msecs)03d:%(levelname)-8s %(message)s")
formatter.datefmt = '%H:%M:%S'
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)