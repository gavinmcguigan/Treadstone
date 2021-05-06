from robot.libraries.BuiltIn import BuiltIn
from robot.errors import DataError
from robot.api import TestData
from robot.libdoc import libdoc 
import os 
import pprint 
from Mods.AppGlobals.setup import LOGIT, get_config

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

def get_keywords(file_name: str):
    # Prob don't need this, libdoc maybe throws an error when no keywords?
    pass 

def get_project_locations(profile='') -> dict:
    # global _PROJECT_TOTALS
    LOGIT.info("")
    LOGIT.info(f"-------------------- Profile {profile} selected -------------------- ")
    LOGIT.info(f"Searching all TEST_LOCATIONS for suites / test cases.")

    counter = 0
    new_locations = {}

    test_locations = get_config().TEST_LOCATIONS
    if not test_locations:
        LOGIT.error(f"No TEST_LOCATIONS defined in config file!!!")
        return {}

    for proj, test_dirs in test_locations.items():
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

def generate_libdocs():
    resource_dirs = get_config().RESOURCE_DIRS
    for dir in resource_dirs:
        print(dir) 
        files = os.listdir(dir)
        for f in files:
            print(f)

    return 

    # generate kw reports.
    # Save to file.  

    print(""" Work in progress, still to find out a few things. """)

    # --- Temp  ---
    whichfile2 = "/Users/gav/Repos/TestRepos/shared-web-test/libs/CleanUp"
    output_file2 = f"{whichfile2}/CleanUp.html"
    libdoc(library_or_resource=whichfile2, outfile=output_file2, name="Cleanup Lib Keywords", version="1.0")


    return

    # Read the config file before checking for keywords. 
    GV.read_config_from_json_file()

    # Loop though libraries / keywords in config file. 
    for libname, dir_list in GV.CFG_LIBRARIES.iteritems():
        for n, lib_dir in enumerate(dir_list):
            libname = libname.replace(" ", "")  # remove spaces from any name that has them. 
            
            name = "{}_{}.html".format(libname, n) if n else "{}.html".format(libname)
            doc_file = create_dirs_if_not_exist_for_libdocs(libname, lib_dir, name)

            # -------------------------------------------------------------------------------- 1. Python libraries
            libdoc(library_or_resource=lib_dir, outfile=doc_file, name=name, version="{} {} Doc.".format(GV.APP_NAME, GV.APP_VER), docformat='ROBOT')
        
            # -------------------------------------------------------------------------------- 2. Robot Kw libraries
            #  Loop through files in lib_dir and check for files that start with kw.
            #  User can put filename in here or directory lib_dir != directory always. 
            
            if os.path.isdir(lib_dir):
                # Dirs
                for each_file in [f for f in os.listdir(lib_dir) if f.startswith('kw_')]:
                    print("Dir file ->  {}".format(each_file))
                
            if os.path.isfile(lib_dir):
                # Files 
                print("File -> {}".format(lib_dir)) 

def display_profile():
    print()
    pp = pprint.PrettyPrinter(indent=2)
    config = get_config()
    pp.pprint(vars(config))