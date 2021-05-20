from robot.libraries.BuiltIn import BuiltIn
from robot.errors import DataError
from robot.api import TestData, ResourceFile
from robot.libdoc import libdoc 
import os 
import pprint
from Treadstone.Mods import setup
import logging

logger = logging.getLogger(__name__)
logger.debug('Init app_funcs.py')
pp = pprint.PrettyPrinter(indent=2)

def get_test_cases(file_name: str) -> list:
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

def check_for_keywords(resource_file: str):
    if not resource_file.endswith('.robot') and not resource_file.endswith('.txt') and not resource_file.endswith('.resource'):
        return []

    resource = ResourceFile(source=resource_file)
    resource.populate()
    keywords = [kw.name for kw in resource.keyword_table]
    return keywords

def get_project_locations(profile='') -> dict:
    # global _PROJECT_TOTALS
    logger.info("")
    logger.info(f"-------------------- Profile {profile} selected -------------------- ")
    logger.info(f"Searching all TEST_LOCATIONS for suites / test cases.")

    counter = 0
    new_locations = {}

    test_locations = setup.get_config().TEST_LOCATIONS
    if not test_locations:
        logger.error(f"No TEST_LOCATIONS defined in config file!!!")
        return {}

    for proj, test_dirs in test_locations.items():
        test_suite_count, test_case_count = 0, 0
        try:
            logger.info("")
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

                logger.info("{}".format(d))
                logger.info("Suites: {:<4} TestCases: {}".format(test_suite_count, test_case_count))

        except OSError:
            logger.error('{} Not found.'.format(d))

    return new_locations

def check_if_test_file(file_name: str) -> int:
    """ Returns True if filename passed in is a test file, otherwise False """
    if not file_name.endswith('.robot') and not file_name.endswith('.txt') and not os.path.isfile(file_name):
        return 0
        
    return len(get_test_cases(file_name=file_name))       

def generate_libdocs():
    """ loops through all the files in the directory passed in, looking for keyword files. """
    resource_dirs = setup.get_config().RESOURCE_DIRS
    
    for name, direct in resource_dirs.items():
        d = direct[0]
        
        print(f'\nChecking -> {d}')

        all_kws = '*** Keywords ***'
        counter = 0

        try:
            listed_dirs = os.listdir(d)
        except FileNotFoundError:
            logger.error(f"{d} not found!")
            continue 

        for f in listed_dirs:
            resource_path = os.path.join(d, f)

            kws = check_for_keywords(resource_path)
            counter += len(kws)

            # print(f'{f} ->  {len(kws)}')

            if kws:
                with open(resource_path, 'r') as openfile:
                    whole_file = openfile.read()

                    x = whole_file.find('*** Keywords ***')
                    y = whole_file.find('*** keywords ***')

                    all_kws += whole_file[x + 16:]

                    # print(f"x {x}   {whole_file[x + 16: x + 40]}")
                    # print(f"y {y}   {whole_file[y: y + 20]}")

        print(f"Keywords found: {counter}")

        # If we found keywords in the files within this directory, do this...
        if counter:
            write_here = os.path.join(setup.SANDBOX_DIR, 'allkws.txt')

            with open(write_here, 'w') as filetowrite:
                filetowrite.writelines(all_kws)

            libdoc(
                library_or_resource=write_here, 
                outfile=os.path.join(setup.LIB_DOC_DIR, f'{name}.html'), 
                name=f'{name}')

        else:
            libdoc(
                library_or_resource=direct[0], 
                outfile=os.path.join(setup.LIB_DOC_DIR, f'{name}.html'), 
                name=f'{name}')

                

    return 

def display_profile():
    print()
    config = setup.get_config()
    pp.pprint(vars(config))


def display_env_vars():
    print()
    config = setup.get_config()
    pp.pprint(vars(config).get('ENV_VARS'))