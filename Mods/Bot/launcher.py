from Mods.AppGlobals.setup import CONFIG, ROBOT_TEST_LOGS, LAUNCH_DIR, LOGIT, switch_profile_gen     # Has to be first import!
from Mods.AppGlobals import app_globals_funcs as GF 
from Mods.Menu.top_menu import TestMenu
from robot import run_cli 
from time import time 
import sys, os

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

def launch_app():
    TL = TestLauncher()

    _PROFILE_GEN = switch_profile_gen()
    default_profile_name, _ = _PROFILE_GEN.__next__()


    menu = TestMenu(default_profile_name)
    
    running = True 

    while running:
        try: 
            while running:
                test_reqs = menu.run()
                
                if isinstance(test_reqs, bool):
                    running = test_reqs

                elif test_reqs == 'Switch Profile':
                    profile_name, _ = _PROFILE_GEN.__next__()
                    menu = TestMenu(profile_name)

                else: 
                    TL.launch_test(*test_reqs)
                    
        except KeyboardInterrupt:
                pass
        finally:   
            print("\n   --- Bye bye! ---\n")
    

