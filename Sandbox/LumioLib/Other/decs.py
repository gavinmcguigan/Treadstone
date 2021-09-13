import functools
import logging
from time import time 
logger = logging.getLogger(__name__)

def assert_profile_results(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        prefix = f"{func.__name__}()"
        starttime = time()
        logger.info(f"{prefix}:  Start")
        result = func(*args, **kwargs)
        logger.info(f"{prefix}:  Result: {str(result)}, {time() - starttime:0.4f} secs")

        # Result should always be a list of tuples with the profile name + the result
        # e.g. [(True, 'Australia'), (False, 'UK'), (True, 'Canada'), (True, 'USA')]

        assert all([n[0] for n in result]) == True

        return result
    
    return wrapper 
