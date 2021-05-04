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
APP_VER = "v1.00.002"

LOGIT = None 

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
LIB_DOC_DIR = os.path.join(LOG_DIR, "LibDocs")
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
    "EXCLUDE": ['Broken'],
    "INCLUDE": [],
    "LISTENERS": [],
    "PYTHONPATH": [LIBRARIES_DIR, RESOURCE_DIR],
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

DEFAULT_CONFIG = SimpleNamespace(**DEFAULTS)
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

def check_for_config_file():
    global CONFIG
    if os.path.isfile(CONFIG_FILE):
        read_json_from_config_file()
        check_json_file()

    else:
        CONFIG = DEFAULT_CONFIG

    write_actual_config_to_file()
    

def read_json_from_config_file():
    global CONFIG
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            CONFIG = SimpleNamespace(**data)
    
    except IOError as ioe:
        LOGIT.error(f"Failed to read from config file: {ioe}")
    except json.decoder.JSONDecodeError:
        LOGIT.error("There's a problem with the config.json file. ")
        
    
def check_json_file():
    global CONFIG
    """ Loop through default config, check that key exists in actual config, if not, add it"""
    
    read_in_config = vars(CONFIG)
    defaul_config_dict = vars(DEFAULT_CONFIG)

    for k, v in defaul_config_dict.items():
        exists = read_in_config.get(k, None)
        if not exists:
            read_in_config[k] = v 

        # Make sure each required config param is what it should be, List or Dict. 
        if k in ["TEST_LOCATIONS", "ENV_VARS"]:
            if not isinstance(exists, dict):
                read_in_config[k] = v

        elif k in ["CHOICES", "EXCLUDE", "INCLUDE", "LISTENERS", "PYTHONPATH", "VARIABLE_FILES"]:
            if not isinstance(exists, list):
                read_in_config[k] = v 


    CONFIG = SimpleNamespace(**read_in_config)

def write_actual_config_to_file():
    # Write config to file in every case? Exists but no chaneg, Changed, Doesn't Exist. 
    try: 
        with open(CONFIG_FILE, 'w+') as f:
            json.dump(vars(CONFIG), f, indent=4, sort_keys=True)
    except IOError as ioe:
        LOGIT.error(f"Failed to write to config file: {ioe}")

        
def config_init():
    create_dirs()
    logger_setup()
    check_for_config_file()

    LOGIT.info(f"")
    desired_length = 60
    gap = desired_length - len(APP_NAME) - len(APP_VER)
    LOGIT.info(f"{APP_NAME}{gap*' '}{APP_VER}")
    LOGIT.info(f"{desired_length*'-'}")

config_init()