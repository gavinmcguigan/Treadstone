from robot.libraries.BuiltIn import BuiltIn
from robot.errors import DataError
from robot.api import TestData
import json
import os 
import sys
import unicodedata
from Mods.AppGlobals.setup import LOGIT, CONFIG


def get_test_cases(file_name=str) -> list:
    """ Returns a list of test cases found in the file passed in.  """
    if not file_name.endswith('.robot') and not file_name.endswith('.txt'):
        return []
    try:
        suite = TestData(source=file_name)
        testcases = [tc.name for tc in suite.testcase_table]         
    except (IOError, UnicodeDecodeError, DataError):
        return []
    else:
        return testcases     

def get_project_locations() -> dict:
    # global _PROJECT_TOTALS
    LOGIT.info("")
    LOGIT.info("Searching all TEST_LOCATIONS for suites / test cases.")

    # Create a list of project objects

    counter = 0
    new_locations = {}
    for proj, test_dirs in CONFIG.TEST_LOCATIONS.items():
        # print "{}".format(test_dirs)
        test_suite_count, test_case_count = 0, 0
        try:
            LOGIT.info("")
            for d in test_dirs:
                
                # ---------------------------------------------------------------------------------- Check for suites and test cases in the project
                for suite in os.listdir(d):
                    res = check_if_test_file(os.path.join(d, suite))
                    if res:
                        test_suite_count += 1
                        test_case_count += res
                
                # ---------------------------------------------------------------------------------- Only add in the case that there are test cases. 
                if test_case_count:
                    counter += 1
                    new_locations[counter] = {"NAME": proj, "LOCATION": d, "SUITES": test_suite_count, "TEST_CASES": test_case_count}

                LOGIT.info("{}".format(d))
                LOGIT.info("Suites: {:<4} TestCases: {}".format(test_suite_count, test_case_count))

        except OSError:
            LOGIT.error('{} Not found.'.format(d))

    return new_locations

def check_if_test_file(file_name: str) -> int:
    """ Returns True if filename passed in is a test file, otherwise False """
    if not file_name.endswith('.robot') and not file_name.endswith('.txt') and not os.path.isfile(file_name):
        return 0
        
    return len(get_test_cases(file_name=file_name))       

# Env variables that can be changed from the command line. 
# def set_envo(environment: str) -> bool:
#     environment = environment.lower()
#     valids = ['ppr', 'dev', 'uat']
#     if environment in valids:
#         GV.WEBENV = environment
#         GV.CFG_ENV_VARS['webenv'] = environment
#         return True
#     LOGIT.debug("Invalid webenv: '{}'.  Valid webenvs: {}".format(environment, str(valids)))
#     LOGIT.debug("WebEnv: {}".format(GV.WEBENV))
#     return False

# def set_accounts(account: str) -> bool:
#     account = account.upper()
#     # ENV_VAR signInMS is set here. 
#     accepted = {'GOOGLE': 'google',
#                 'GOOG': 'google',
#                 'MS': 'microsoft',
#                 'MICROSOFT': 'microsoft'}

#     val = accepted.get(account, False)
#     if val:
#         GV.ACCOUNTS = val
#         if GV.ACCOUNTS == 'google':
#             GV.CFG_ENV_VARS['SIGNINMS'] = False
#         else:
#             GV.CFG_ENV_VARS['SIGNINMS'] = True         
#         return True
    
#     LOGIT.debug("Invalid Account: '{}'.  Valid BRANCHES: {}".format(account, str(accepted.keys())))
#     LOGIT.debug("Accounts: {}".format(GV.ACCOUNTS))
#     return False

# def set_branch(branch: str) -> bool:
    # branch = branch.lower()
    # accepted = {'dev': 'develop',
    #             'develop': 'develop',
    #             'master': 'master',
    #             'mast': 'master',
    #             'orlando': 'orlando',
    #             'orl': 'orlando'}

    # val = accepted.get(branch, False)

    # if val:
    #     GV.BRANCH = val 
    #     GV.CFG_ENV_VARS['BRANCH'] = val
    #     return True
    # LOGIT.debug("Invalid Branch: '{}'.  Valid BRANCHES: {}".format(branch, str(accepted.keys())))
    # GV.LOGIT.debug("Branch: {}".format(GV.BRANCH))
    # return False