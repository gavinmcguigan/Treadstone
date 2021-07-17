import os, sys
import shutil
from robot.api import logger
import requests, functools 

UPLOAD_URL_ENDPOINT = 'http://127.0.0.1:5002'
DOWNLOAD_FOLDER = '/Users/gav/Repos/TestRepos/Treadstone/Sandbox/ChromeProfiles/downloads'


R = None

def _request_decorator(func):
    @functools.wraps(func)
    def request_decorator_wrapper(*args, **kwargs):
        """ Should always return a dictionary. """
        global R 
        # req_list = ['url', 'verify', 'data', 'headers', 'payload', 'cookies', 'timeout', 'auth', 'params']
        # new_kwargs = {k:v for k, v in kwargs.items() if k in req_list}    
        kwargs['headers'] = {'User-agent': f'Python-Stripe-Lib/{requests.__version__}'}
        if 'timeout' not in kwargs:
            kwargs['timeout'] = (5, 30)
        try:
            R = func(*args, **kwargs)
            logger.info(f"{(func.__name__).upper()} -> {kwargs.get('url')}: {R.status_code}")
            print(f"{(func.__name__).upper()} -> {kwargs.get('url')}: {R.status_code}")

            if 'application/json' in R.headers.get('content-type'):
                js = R.json()
                print(f"Json: {js}")
            else:
                js = {}
        
        except requests.exceptions.Timeout:
            raise Exception(f"Connection Timeout of {kwargs.get('timeout')[0]} secs reached! ")
        
        except requests.exceptions.ConnectionError:
            raise Exception(f"Couldn't reach: {kwargs.get('url')}")
        
        except ValueError as ve:
            raise Exception(f"{ve}")

        except KeyboardInterrupt as ki:
            raise Exception(f"{ki}")
        else:
            
            return R, js 

    return request_decorator_wrapper  


@_request_decorator
def post(*args, **kwargs):
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


def zip_profile(folderpath):
    if os.path.exists(folderpath):
        zipped_filepath = shutil.make_archive(f"{folderpath}", 'zip', folderpath)
        return zipped_filepath

def post_profile(zipped_filepath, email):
    with open(zipped_filepath, 'rb') as zf:
        post(url=f"{UPLOAD_URL_ENDPOINT}/profile", stream=True, params={'email': email}, files= {'file': zf})

def get_profile(folder):
    get(url=f"{UPLOAD_URL_ENDPOINT}/profile/{folder}", stream=True, timeout=(10, 30))

    if R.status_code == 200:
        total_length = R.headers.get('content-length')
        
        if total_length:
            dl = 0
            total_len = int(total_length)
            zip_file = os.path.join(DOWNLOAD_FOLDER, f"{folder}.zip")
            print(f'Receiving file: {zip_file}')
            print(f"Size: {total_length}")
            with open(zip_file, 'wb') as f:
                for data in R.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_len)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()

            print(f'\nFile downloaded successfully!')