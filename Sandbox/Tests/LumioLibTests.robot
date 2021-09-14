*** Settings ***
Library             LumioLib
Library             BuiltIn
Library             LumioLib.ClassLibs.ClassOne
#Library             LumioLib.InheritSeleniumLibrary.InheritSeleniumLibrary
#Library             /Users/gav/Repos/TestRepos/Treadstone/Sandbox/LumioLib/ClassLibs/InheritSeleniumLibrary.py
#Library             /Users/gav/Repos/TestRepos/Treadstone/Sandbox/LumioLib/ClassLibs/Decomposition.py
Library             LumioLib.InheritSeleniumLibrary
*** Variables ***


*** Test Cases ***
Delete Server Side Chrome Profile 
    Delete Chrome Profile From Server   gavinmcguigan.teacher@smartwizardschool.com

Download A User Chrome Profile 
    Download Chrome Profile     gavinmcguigan.student1@smartwizardschool.com

Get All Zip Files Available For Chrome Profiles
    Get List Of Zips Available 

Get All Chrome Profiles On The Server
    Get Profile Accounts

#Fill In Purchase Form 
#    Go To Purchase Form And Fill In

Open Chrome Profile With Create Web Driver
    ${options}=       Download Chrome Profile     gavinmcguigan.teacher@smartwizardschool.com
    ${browser_id}=    Create WebDriver    Chrome    chrome_options=${options}
    &{all libs}=    Get Library Instance    all=True
    Log     ${all libs}
    Log     ${browser_id}
    Go To   chrome://version/
    Sleep  5
    Close All Browsers
    #Profile Login Teacher       ${user_email}   ${user_pass}    ${url}


Open Chrome Profile With Inherited Selenium Library 
    Open Chrome Profile Browser
    #Open Browser  google  
    Sleep  2
    Close All Browsers


Open Chrome Profile With Web Driver
    ${browser_id}=  Open Browser With Chrome Profile    gavinmcguigan.teacher@smartwizardschool.com
    &{all libs}=    Get Library Instance    all=True
    Log     ${all libs}
    Log     ${browser_id}
    Go To   chrome://version/
    Sleep  5
    Close All Browsers


Open Browser Normal 
    ${browser_id}=  Open Browser    google
    &{all libs}=    Get Library Instance    all=True
    Log     ${all libs}
    Log     ${browser_id}
    Go To   chrome://version/
    Sleep  5
    Close All Browsers