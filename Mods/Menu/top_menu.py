from Treadstone.Mods import setup 
from Treadstone.Mods import app_funcs
from os import path, listdir  

import logging
logger = logging.getLogger(__name__)
logger.debug('Init top_menu.py')

  
class TestMenu():
    def __init__(self, profile_name):
        self.profile = profile_name[:-5]
        self.project_locations = app_funcs.get_project_locations(profile_name)     # 
        self.where_we_are = 'PROJECTS'                          # Can be PROJECTS, TEST_SUITES or TEST_CASES
        self.project, self.test_suite, self.test_case = None, None, None 
        self.display_options = self.project_locations 
        self.test_just_ran = False
        self.dont_show_menu = False 

    def run(self):
        """ Stays in this while loop until a testcase / test suite // test folder is selected. """ 
        self.test_case = None           # After test is run, test_case gets reset. 
        self.test_just_ran = True       # Reset after test run.  Stops the clear screen.

        while True:
            if not self.project_locations:
                logger.info(f"   Profile '{self.profile}'' has no test cases at the TEST_LOCATIONS provided!!!")
                return 'Switch Profile'

            if setup.get_config().CHOICES:
                choice = str(setup.get_config().CHOICES.pop(0))
                if choice in ['Q', 'q']:
                    break

                elif choice in ['p', 'P']:
                    self.dont_show_menu = True 
                    return "Switch Profile"  # Also exits if switching profile. 

                else:
                    if self.parse_cmd(choice):
                        continue    # Does what it has to do and goes back to the start of the loop. 
                
                if self.parse_menu_option(choice):
                    proj_name = self.project_locations[self.project]["NAME"]
                    proj_dir = self.project_locations[self.project]["LOCATION"]
                    return proj_name, proj_dir, self.test_suite, self.test_case             

            else:
                # if self.dont_show_menu:
                self.display_contents()
                self.test_just_ran = False
                self.get_user_choices()
                self.dont_show_menu = False 
        
        return False                                       # Only reaches here when q is pressed. 

    def parse_menu_option(self, choice):
        suite_selected = False 
        
        if choice == "*" and self.where_we_are != 'PROJECTS':         # When * is used, return True, Test case won't be set, so runs the full suite.  
            return True 
        
        elif choice.startswith("*"):
            choice = choice.replace('*', '')
            suite_selected = True 
        
        try:
            choice = int(choice)
        except ValueError:
            pass
        else:
            if choice in range(len(self.display_options) + 1):          # Make sure option is in range
                if self.where_we_are == 'PROJECTS':
                    self.is_project(choice)

                elif self.where_we_are == 'TEST_SUITES':
                    self.is_test_suite(choice)
                    return suite_selected           # When * is used, returns True, Test case won't be set, so runs the full suite. 
                else:                                       
                    self.is_test_case(choice)
                    return True

        return False

    def parse_cmd(self, cmd):
        if cmd == 'b':
            self.move_back()
            return True

        elif cmd == '#':
            app_funcs.generate_libdocs() 
            self.test_just_ran = True
            return True 
        
        elif cmd == 'profile':
            app_funcs.display_profile()
            self.test_just_ran = True
            return True 

        elif cmd == 'vars':
            app_funcs.display_env_vars()
            self.test_just_ran = True 
            return True 

        else:
            logger.debug('{}'.format(cmd))

        return False 

    def is_project(self, usr_choice):
        """ Set where_we_are, set the project & set the display options. """
        self.where_we_are = "TEST_SUITES"
        self.project = usr_choice  
        loc = self.project_locations[self.project]["LOCATION"]
        self.display_options = sorted([f for f in listdir(loc) if app_funcs.check_if_test_file(path.join(loc, f))])       

    def is_test_suite(self, usr_choice):
        """ Set where_we_are, set the test suite & set the display options. """
        self.where_we_are = "TEST_CASES"
        self.test_suite = self.display_options[usr_choice - 1]
        self.display_options = app_funcs.get_test_cases(path.join(self.project_locations[self.project]["LOCATION"], self.test_suite))
        
    def is_test_case(self, usr_choice):
        """ Set Test Case """
        self.test_case = self.display_options[usr_choice - 1] 

    def get_user_choices(self):  
        print('')
        choice = input(f'   {self.profile} > ')
        if choice:
            for ch in choice.split(' '):
                setup.get_config().CHOICES.append(ch)

    def move_back(self):     
        """ Moves back in the menu and sets the variables for new location. """
        if self.where_we_are == "TEST_SUITES":
            self.project = None 
            self.where_we_are = "PROJECTS"
            self.display_options = self.project_locations 
                        
        elif self.where_we_are == "TEST_CASES":
            self.test_suite = None
            self.where_we_are = "TEST_SUITES"
            loc = self.project_locations[self.project]["LOCATION"]
            self.display_options = sorted([f for f in listdir(loc) if app_funcs.check_if_test_file(path.join(loc, f))]) 
                       
        else:   # == "PROJECTS"
            pass 
        
    def display_contents(self):
        print("\n")
        if not self.test_just_ran:
            print("\033[H\033[J")      
        
        header_len = 90

        if self.where_we_are == "PROJECTS":
            header = "   {} {}".format(setup.APP_NAME, setup.APP_VER)
            offset = header_len - len(header) - len(self.where_we_are)
            header = "{}{}{}".format(header, offset*' ', self.where_we_are)

            print(header)
            print("{}{}".format('   ', (len(header)-3)*'-'))
            print

            for k, v in self.display_options.items():
                print("   {}. {}".format(k, v['NAME']))
            

        elif self.where_we_are == "TEST_SUITES":
            project_name = self.project_locations[self.project]['NAME']
            header = "   {}".format(project_name)
            offset = header_len - len(header) - len(self.where_we_are)
            header = "{}{}{}".format(header, offset*' ', self.where_we_are)

            print(header)
            print("{}{}".format('   ', (len(header)-3)*'-'))
            print
       
            for n, each in enumerate(self.display_options):
                print("   {}. {}".format(n+1, each))
            
            
            # contents_to_show = [" -> ".join(p.split('/')[-3:]) for p in self.display_options]
        elif self.where_we_are == "TEST_CASES":      
            project_name = self.project_locations[self.project]['NAME']
            header = "   {}  ->  {}".format(project_name, self.test_suite)
            offset = header_len - len(header) - len(self.where_we_are)
            header = "{}{}{}".format(header, offset*' ', self.where_we_are)

            print(header)
            print("{}{}".format('   ', (len(header)-3)*'-'))
            print
       
            for n, each in enumerate(self.display_options):
                print("   {}. {}".format(n+1, each))
        print
