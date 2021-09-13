import pprint
from robot.api import logger
import requests, functools 

def _request_decorator(func):
    @functools.wraps(func)
    def request_decorator_wrapper(*args, **kwargs):
        """ Should always return a dictionary. """
        req_list = ['url', 'verify', 'data', 'headers', 'payload', 'cookies', 'timeout', 'auth', 'params']
        new_kwargs = {k:v for k, v in kwargs.items() if k in req_list}    
        new_kwargs['headers'] = {'User-agent': f'Python-Stripe-Lib/{requests.__version__}'}
        if 'timeout' not in new_kwargs:
            new_kwargs['timeout'] = (5, 30)
        try:
            r = func(*args, **new_kwargs)
            logger.info(f"{(func.__name__).upper()} -> {new_kwargs.get('url')}: {r.status_code}")
            js = r.json()
        
        except requests.exceptions.Timeout:
            raise Exception(f"Connection Timeout of {new_kwargs.get('timeout')[0]} secs reached! ")
        
        except requests.exceptions.ConnectionError:
            raise Exception(f"Couldn't reach: {new_kwargs.get('url')}")
        
        except ValueError as ve:
            raise Exception(f"{ve}")

        except KeyboardInterrupt as ki:
            raise Exception(f"{ki}")
        else:
            return r, js 

    return request_decorator_wrapper  


@_request_decorator
def post(*args, **kwargs):
    if not kwargs.get('stream', False):
        kwargs['stream'] = True 
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
