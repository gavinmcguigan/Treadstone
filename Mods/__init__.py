import logging
from logging.handlers import RotatingFileHandler
import os 
from pathlib import Path 

APP_NAME = "Treadstone" 
APP_VER = "v1.01.000"
p = Path(os.path.dirname(os.path.realpath(__file__)))
launch_dir = p.parent 
APP_LOG_FILE = os.path.join(launch_dir, "{}.log".format(APP_NAME))


class TreadstoneFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        RotatingFileHandler.__init__(self, *args, **kwargs)
        fs = "%(asctime)s.%(msecs)03d:%(levelname)-8s %(name)-25s   %(message)s"
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


logger = logging.getLogger(__name__)
handler = TreadstoneFileHandler(APP_LOG_FILE, mode='a', maxBytes=10000, backupCount=1, delay=0)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.warning('Warning')
logger.error('error')
logger.critical('critical')
logger.info('info')
logger.debug('debug')

logger.info('\n\n')
logger.info(f"{90*'*'}")
desired_length = 80
gap = desired_length - len(APP_NAME) - len(APP_VER)
logger.info(f"{APP_NAME}{gap*' '}{APP_VER}")
logger.info(f"{desired_length*'-'}")

from .AppGlobals import setup
from .AppGlobals import app_funcs  
from .Menu import top_menu
from .Bot import launcher

logger.info('-')

setup.config_init()


"""
Treadstone 
    launch.py
    
    Mods    
        __init__.py

        AppGlobals
            app_globals_funcs.py
            setup.py 
        Bot
            launcher.py
        Menu
            top_menu.py
        Vars
            env_vars.py 


"""

