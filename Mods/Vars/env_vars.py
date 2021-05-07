from Mods.AppGlobals.setup import LOGIT, get_config
import sys 
import os
from time import time 

def get_variables():
    """ Takes in the app CFG_ENV_VARS and passes it to the robot api when launching tests. """
    # for k, v in GV.CFG_ENV_VARS.items():
    #     GV.CFG_ENV_VARS.setdefault(k, v)             # Should set the key value, only if it doesn't exist. 
    for k, v in get_config().ENV_VARS.items():
        LOGIT.debug("-v  {}:{}".format(k, v))
    LOGIT.debug("")

    return get_config().ENV_VARS
