from logging.handlers import RotatingFileHandler
from platform import uname
from collections import deque
import logging 
import os 
import sys
from pathlib import Path 
import json 
from types import SimpleNamespace

p = Path(os.path.dirname(os.path.realpath(__file__)))
LAUNCH_DIR = p.parent.parent
APP_NAME = "Treadstone" 
APP_VER = "v1.01.000"

LOGIT = None 
TEST_REPOS = [
    'content-portal-test',
    'identity-test',
    'lab-static-test',
    'lab-web-test',
    'labc-test',
    'notebook-test',
    'session-test',
    'shared-web-test',
    'slso-suite-test', 
    ]

# -------------------------------------------------------------------------------------- Directories
SANDBOX_DIR = os.path.join(LAUNCH_DIR, 'Sandbox')

TESTS_DIR = os.path.join(SANDBOX_DIR, "Tests")
LISTENERS_DIR = os.path.join(SANDBOX_DIR, "Listeners")
LIBRARIES_DIR = os.path.join(SANDBOX_DIR, "Libs")
VARFILE_DIR = os.path.join(SANDBOX_DIR, "VariableFiles")
CONFIG_DIR = os.path.join(SANDBOX_DIR, "Config")
SCRIPT_DIR = os.path.join(SANDBOX_DIR, "Scripts")
RESOURCE_DIR = os.path.join(SANDBOX_DIR, "Resources")
LOG_DIR = os.path.join(SANDBOX_DIR, 'Logs')
ROBOT_TEST_LOGS = os.path.join(LOG_DIR, "RobotTestLogs")
LIB_DOC_DIR = os.path.join(SANDBOX_DIR, "LibDocs")
REPO_DIR = os.path.dirname(LAUNCH_DIR)       

TREADSTONE_LOG = os.path.join(LOG_DIR, "{}Log".format(APP_NAME))
CONFIG_FILE = os.path.join(CONFIG_DIR, "{}.json".format(APP_NAME))
APP_LOG_FILE = os.path.join(TREADSTONE_LOG, "{}.log".format(APP_NAME))

def get_os_run():
    op_sys = sys.platform 
    if 'darwin' in op_sys:
        op_sys = 'mac'
    elif 'win' in op_sys:
        op_sys = 'win'

    return op_sys

PROFILES = []

DEFAULTS = { 
    "ENV_VARS": {
        "BRANCH": "develop",
        "BROWSER": "gc",
        "FORCE_ENABLE_APPLITOOLS": False,
        'OSRUN': get_os_run(),
        'MACHINE_NAME': uname()[1],
        "MSBRANCH": "learning",
        "REGION": "global",
        "SIGNINMS": False,
        "WEBENV": "dev"
    },
    "EXCLUDE": [],
    "INCLUDE": [],
    "LISTENERS": [],
    "PYTHONPATH": [LIBRARIES_DIR, RESOURCE_DIR],
    "RESOURCE_DIRS": {
        "Treadstone": [RESOURCE_DIR],
        "Content-Portal-Test": [os.path.join(REPO_DIR, "content-portal-test", "keywords")],
        "Identity-Test": [os.path.join(REPO_DIR, "identity-test", "keywords")],
        "Session-Test": [os.path.join(REPO_DIR, "session-test", "keywords")],
        "Shared-Desktop-Test": [os.path.join(REPO_DIR, "shared-desktop-test", "keywords")],
        "Shared-Web-Test": [os.path.join(REPO_DIR, "shared-web-test", "keywords")],
        "SLSO-Suite-Test": [os.path.join(REPO_DIR, "slso-suite-test", "keywords")],
        "Shared-Test": [os.path.join(REPO_DIR, "shared-test", "keywords")],
    },
    "CHOICES": [],
    "TEST_LOCATIONS": {
        APP_NAME: [TESTS_DIR],
        "Content-Portal-Test": [os.path.join(REPO_DIR, "content-portal-test", "tests")],
        "Identity-Test": [os.path.join(REPO_DIR, "identity-test", "tests")],
        "Lab-Static-Test": [os.path.join(REPO_DIR, "lab-static-test", "tests")],
        "Labc-Test": [os.path.join(REPO_DIR, "labc-test", "tests")],
        "Notebook-Test": [os.path.join(REPO_DIR, "notebook-test", "tests")],
        "Session-Test": [os.path.join(REPO_DIR, "session-test", "tests")],
        "Shared-Desktop-Test": [os.path.join(REPO_DIR, "shared-desktop-test", "tests")],
        "Shared-Web-Test": [os.path.join(REPO_DIR, "shared-web-test", "tests", "training")],
        "SLSO-Test-Suite": [os.path.join(REPO_DIR, "slso-suite-test", "tests")],
    },
    "VARIABLE_FILES": []
}

# DEFAULT_CONFIG = SimpleNamespace(**DEFAULTS)
CONFIG = {}


def create_dirs():
    CREATE_DIRS = {
        SANDBOX_DIR: [TESTS_DIR, LISTENERS_DIR, LIBRARIES_DIR, VARFILE_DIR, CONFIG_DIR, SCRIPT_DIR, RESOURCE_DIR],
        LOG_DIR: [ROBOT_TEST_LOGS, LIB_DOC_DIR, TREADSTONE_LOG]}

    for k, directories in CREATE_DIRS.items():
        try:
            os.mkdir(k)
        except OSError:
            pass
        
        for directory in directories:
            try:
                os.mkdir(directory)
            except OSError:
                pass
class TreadstoneFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        RotatingFileHandler.__init__(self, *args, **kwargs)
        fs = "%(name)s  %(asctime)s.%(msecs)03d %(levelname)-5s >  %(message)s"
        formatter = logging.Formatter(fs)
        formatter.datefmt = '%H:%M:%S'
        self.setFormatter(formatter)
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        try:
            msg = self.format(record)
            self.stream.write(msg)
            self.stream.write('\n')
            self.flush()

        except Exception:
            self.handleError(record)

def logger_setup():
    global LOGIT 
    LOGIT = logging.getLogger(APP_NAME.upper())
    LOGIT.setLevel(logging.DEBUG)
    handler = TreadstoneFileHandler(APP_LOG_FILE, mode='a', maxBytes=10000, backupCount=1, delay=0)
    LOGIT.addHandler(handler)

def check_for_profiles():
    global PROFILES
    PROFILES = {f: os.path.join(CONFIG_DIR, f) for f in os.listdir(CONFIG_DIR) if f.endswith('.json')}

    # Check profiles have defaults. 
    for profile, profile_path in PROFILES.items():
        json_data = read_json_from_config_file(profile_path)
        modified_json = check_json_data(json_data)
        write_actual_config_to_file(profile_path, modified_json)

def check_for_config_file():
    global CONFIG 
    # default CONFIG_FILE has to exist, check if exists, if not create it. 
    if os.path.isfile(CONFIG_FILE):
        json_data = read_json_from_config_file(CONFIG_FILE)
        modified_json = check_json_data(json_data)
        write_actual_config_to_file(CONFIG_FILE, modified_json)
        
    else:
        write_actual_config_to_file(CONFIG_FILE, DEFAULTS)

def read_json_from_config_file(which_file):
    try:
        with open(which_file, 'r') as f:
            data = json.load(f)
    
    except IOError as ioe:
        LOGIT.error(f"Failed to read from config file: {ioe}")
        return {}
    except json.decoder.JSONDecodeError:
        return {}
    else:
        return data
        
def check_json_data(read_in_config):
    """ Loop through default config, check that key exists in config file, if not, add it. """
    
    for k, v in DEFAULTS.items():
        # If the key doesn't exist, add it + the default value. 
        if k not in read_in_config: 
            read_in_config[k] = v 

        # Looks for key (k) and returns it's value or None if doesn't exist. 
        value = read_in_config.get(k, None)

        # If value is not a dict, make it the default dict. 
        if k in ["TEST_LOCATIONS", "ENV_VARS"]:
            if not isinstance(value, dict):
                read_in_config[k] = v

        # If value is not a list, make it the default list. 
        elif k in ["CHOICES", "EXCLUDE", "INCLUDE", "LISTENERS", "PYTHONPATH", "VARIABLE_FILES"]:
            if not isinstance(value, list):
                read_in_config[k] = v

    return read_in_config 

def write_actual_config_to_file(which_file, data):
    # Write config to file in every case? Exists but no chaneg, Changed, Doesn't Exist. 
    # CONFIG = SimpleNamespace(**data)

    try: 
        with open(which_file, 'w+') as f:
            json.dump(data, f, indent=4, sort_keys=True)
    except IOError as ioe:
        LOGIT.error(f"Failed to write to config file: {ioe}")

def switch_profile_gen():
    global CONFIG
    LOGIT.info(f'{len(PROFILES)} Profiles Initiated')
    while True:
        for profile, profile_path in PROFILES.items():
            LOGIT.info(f"{profile}: {profile_path}")
            json_data = read_json_from_config_file(profile_path)
            modified_json = check_json_data(json_data)
            write_actual_config_to_file(profile_path, modified_json)
            CONFIG = SimpleNamespace(**modified_json)
            LOGIT.debug("")
            LOGIT.debug(f"{80*'-'}")
            for envvar, value in CONFIG.ENV_VARS.items():
                LOGIT.debug(f" {envvar}:  {value}")
            yield profile, profile_path 

def get_config():
    global CONFIG     
    return CONFIG 

def config_init():
    create_dirs()
    logger_setup()

    # Check default profile/config exists
    check_for_config_file()
    
    # Get profiles and add to profile dict
    check_for_profiles()

    LOGIT.info(f"")
    desired_length = 60
    gap = desired_length - len(APP_NAME) - len(APP_VER)
    LOGIT.info(f"{APP_NAME}{gap*' '}{APP_VER}")
    LOGIT.info(f"{desired_length*'-'}")

config_init()


"""


"""