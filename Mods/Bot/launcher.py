from Mods.AppGlobals import setup 
from Mods.AppGlobals.setup import CONFIG, ROBOT_TEST_LOGS, LAUNCH_DIR, LOGIT, APP_NAME, APP_VER     # Has to be first import!
from Mods.AppGlobals import app_globals_funcs as GF 
from Mods.Menu.top_menu import menu_setup
from robot import run_cli 
from robot.libdoc import libdoc 
from time import time, sleep 
from datetime import timedelta, datetime
import sys
import os 
from threading import Thread 


class TestLauncher:
    def __init__(self):
        self.common = None
        self.user_args = sys.argv[1:]
        self.outputdir = None

    def set_log_output_dir(self, project_name=None, test_file=None):
        """ Set the log output directory based on the suite / test case passed in. """
        if test_file is not None:
            self.outputdir = os.path.join(ROBOT_TEST_LOGS, test_file.replace('.robot', ''))
            self.outputdir = os.path.join(ROBOT_TEST_LOGS, test_file.replace('.txt', ''))
        else:
            self.outputdir = os.path.join(ROBOT_TEST_LOGS, project_name)
        
        self.common += ["--outputdir", self.outputdir]
        LOGIT.info(f"--outputdir     {self.outputdir}")

    def add_variables(self):
        """ Add env variables from config file. """
        for k, v in CONFIG.ENV_VARS.items(): 
            self.common += ["--variable", f"{k}:{v}"]
            LOGIT.info(f'--variable      {k}:{v}')

    def add_variable_files(self):
        """ Global variables hold the variables taken from the Treadstone.json file 
            App requires env_vars.py, so it will always be included. """
        envvars = os.path.join(LAUNCH_DIR, "Mods", "Vars", "env_vars.py")
        self.common += ["--variablefile", envvars]
        for vf in CONFIG.VARIABLE_FILES:
            self.common += ["--variablefile", vf]
            LOGIT.info(f'--variablefile  {vf}')
    
    def add_include_tags(self):
        """ Global variable holds all the include tags taken from the Treadstone.json file """
        for tag in CONFIG.INCLUDE:
            self.common += ["--include", tag]
            LOGIT.info(f'--include       {tag}')

    def add_exclude_tags(self):
        """ Global variable holds all the exclude tags taken from the Treadstone.json file """
        for tag in CONFIG.EXCLUDE:
            self.common += ["--exclude", tag]
            LOGIT.info(f'--exclude       {tag}')

    def add_listeners(self):
        """ Add listener path locations from config file. 
        Splunk listener: "/Users/gav/Repos/TestRepos/shared-test/tools/rf_listener/10.0/tcListener_url.py:bt:buildidtest:test_output_dir:test_outer_suite:subdir_test", 
        """
        for l in CONFIG.LISTENERS:
            # self.common += ['--listener', '/Users/gav/Repos/TestRepos/shared-test/tools/rf_listener/10.0/tcListener_url.py']
            self.common += ['--listener', l]
            LOGIT.info(f'--listener      {l}')

    def add_python_paths(self):
        """ Add any paths from the config file to --pythonpath args"""
        for pth in CONFIG.PYTHONPATH:
            self.common += ["--pythonpath", pth]
            LOGIT.info(f'--pythonpath    {pth}')

    def add_test_case(self, test_case):
        """ If user selects a test case, append to common. """
        if test_case is not None:
            self.common += ['--test', test_case]
            LOGIT.info(f"--test          {test_case}")

    def add_proj_dir(self, project_dir=None, test_file=None):
        """ Add any other args passed in by the user, then append the test file or test dir as the last arg. """             
        self.common += self.user_args
        if test_file is not None:
            self.common.append(os.path.join(project_dir, test_file))
        else:
            self.common.append(project_dir)

    def launch_test(self, project_name=None, project_directory=None, test_file=None, test_case=None):
        """ Reset the common var, then step by step add output dir, variable files, include an exclude tags, 
            test case, and finally the project dir or test suite. """

        starttime = time()
        LOGIT.info("-----------> Launching Test <-----------")

        self.common = [
            '--log', 'a_testlog.html', 
            '--debugfile', 'debugfile.log',
            '--loglevel', 'INFO',
            # '--exitonfailure',                         # Stops test execution if any critical test fails. Suite/Test tear downs are still executed. 
            # '--exitonerror',                           # Will stop test execution if any errors occurs when parsing test data, importing libraries etc.
            '--console', 'verbose',
            '--consolemarkers', 'on',
            '--consolecolors', 'on',
            ]

        self.set_log_output_dir(project_name, test_file)
        # self.add_variables()
        self.add_variable_files()
        self.add_include_tags()
        self.add_exclude_tags()
        self.add_listeners()
        self.add_python_paths()
        self.add_test_case(test_case)
        self.add_proj_dir(project_directory, test_file)

        LOGIT.debug(f"{self.common}".format(str(self.common)))

        test_result = run_cli(self.common, exit=False)
        LOGIT.info(f"-----------> Test Result: {test_result} <-----------  Time Taken: {time()-starttime:0.3f} secs")



def generate_libdocs():
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

def launch_test_case():
    TL = TestLauncher()
    runner = menu_setup()

    if runner:
        try: 
            while True:
                test_reqs = runner()
                
                if not isinstance(test_reqs, tuple):
                    if not test_reqs: # Return False
                        break
                    if test_reqs == 'Documentation':
                        generate_libdocs()
                else: 
                    TL.launch_test(*test_reqs)
                    
        except KeyboardInterrupt:
                pass
        finally:   
            print("\n   --- Bye bye! ---\n")
    

