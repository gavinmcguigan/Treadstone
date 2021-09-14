from time import sleep, time 
from robot.api import logger
from selenium.common.exceptions import NoSuchElementException
from LumioLib.WebDriver import get_lib_instance
import traceback, sys

def find_an_element(list_of_elements, email, password, class_code, lib_inst, timeout=60, retry=0.5):
    starttime = time()
    
    while time() - starttime < timeout:
        for xpath, descriptor, action in list_of_elements:
            
            try: 
                # el = lib_inst.find_element(xpath)
                el = lib_inst.find_element_by_xpath(xpath)
            except Exception:
                sleep(retry)
                # traceback.print_exc(file=sys.stdout)
            else:
                sleep(1)
                logger.info(f'{descriptor}.')  
                if action is None:
                    return False

                elif action == "click":
                    el.click()
                    
                elif action in ["email", "password"]:
                    el.clear()
                    k = email if action == "email" else password
                    el.send_keys(k)
                    find_an_element([("//span[contains(text(),'Next')]", "Next Button", "click")], email, password, class_code, lib_inst)
                    sleep(3)
                
                elif action == "class_code":
                    el.clear()
                    el.send_keys(f"{class_code}")

                return True

    raise NoSuchElementException(f'None of the elements expected were found.')

def _login_to_lumio(email, user_password, url, element_expected="//img[@class='profile-picture']", class_code=None, lib_inst=None):
    logger.info(f'Go to: {url}')

    if lib_inst:
        lib_inst.get(url)
    else:
        lib_inst = get_lib_instance()
        lib_inst.go_to(url)

    teacher_login = [
        (element_expected, "Library", None),
        ("//input[(@name='password')]", f"Enter Password", "password"),
        ("//input[(@id='identifierId' and @type='email')]", f"Enter Email", "email"),
        ("//input[(@id='complete')]", f"More About You", "click"),
        (f"//span[contains(text(), '{email}')]", f"Welcome Back", "click"),
        ("//button[contains(text(), 'Teacher sign in')]", f"Teacher Sign In", "click"),
        ("//*[@class='instructions' and contains(text(), 'Sign in with Google')]", f"Sign In With Google", "click"),
        ("//div[contains(@class, 'v-btn__content')]", f"Confirm Location", "click"),
        (f"//div[contains(@data-identifier, '{email}')]", f"Choose an account", "click"),
        
    ]

    student_login = [
        ("//i[@class='leave-class-icon']", "Waiting for teacher", None),
        ("//div[contains(@class, 'v-btn__content')]", f"Confirm Location", "click"),
        # ("//button[contains(text(),'Next')]", f"Click Next", "click"),
        ("//input[(@id='identifierId')]", f"Enter Email", "email"),
        ("//input[(@name='password')]", f"Enter Password", "password"),
        ("//button[contains(text(), 'Join')]", "After entering class code, press join", "click" ),
        ("//button[contains(text(), 'Sign In')]", "Sign In Button", "click"),
        ("//button[contains(text(), 'Sign in')]", "Sign in button on the sign in as a guest page", "click"),
        (f"//span[contains(text(), '{email}')]", f"Welcome Back", "click"),
        ("//*[@class='instructions' and contains(text(), 'Sign in with Google')]", f"Sign In With Google", "click"),
        (f"//div[contains(@data-identifier, '{email}')]", f"Choose an account", "click"),
        (f"//span[@class='code' and contains(text(), '{class_code}')]", f"Select a class to join", 'click'),
        ("//input[@aria-label='Enter class I D']", "Enter Class ID", "class_code"),

    ]

    # //button[contains(text(), "Join as a guest")]


    flow_options = student_login if class_code else teacher_login
    
    not_found = True
    while not_found:
        not_found = find_an_element(flow_options, email, user_password, class_code, lib_inst)

    print(f'Element Expected: {element_expected} found!')