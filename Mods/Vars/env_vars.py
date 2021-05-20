import sys 
import os
from time import time 
from Treadstone.Mods import setup

import logging
logger = logging.getLogger(__name__)
logger.debug('Init env_vars.py')


def get_variables():
    """ Takes in the app CFG_ENV_VARS and passes it to the robot api when launching tests. """
    # for k, v in GV.CFG_ENV_VARS.items():
    #     GV.CFG_ENV_VARS.setdefault(k, v)             # Should set the key value, only if it doesn't exist. 
    for k, v in setup.get_config().ENV_VARS.items():
        logger.debug("-v  {}:{}".format(k, v))
    logger.debug("")

    return setup.get_config().ENV_VARS
