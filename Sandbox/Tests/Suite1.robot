#!/usr/bin/env robot

*** Settings ***
#Suite Setup         bla bla
#Suite Teardown      bla bla
#Test Setup          bla bla
#Test Teardown       bla bla
#Force Tags          Tag1 Tag2 Tag3

Documentation       Suite to Learn the BuiltIn Keywords from RobotFrameWork
Test Teardown       Run Keyword     Close All Browsers
Library             CustomKeywords

# Library             AutoItLibrary
Library             Selenium2Library
# Library             SeleniumLibrary
Library             OperatingSystem
Library             String
Library             Collections
Library             DateTime
Library             Dialogs
Library             BuiltIn
Library             Process
Library             pabot.PabotLib
Library             /Users/gav/Repos/TestRepos/slso-suite-test/libs/kw_slso_suite.py
# Library             /Users/gav/Repos/TestRepos/shared-web-test/libs/applitools/RobotAppEyesEx.py
Library 	        /Users/gav/Repos/TestRepos/shared-web-test/keywords/identity/kw_json_list_validator.py
Resource            /Users/gav/Repos/TestRepos/slso-suite-test/keywords/__ss_include.txt
Resource            /Users/gav/Repos/TestRepos/slso-suite-test/keywords/__lw_include.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/applitools_eyes/__appeyes_include.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/canvas/__cv_include.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/dashboard/__db_include.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/General/__gnrl_include.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/General/kw_pixelcolour.txt
Resource            /Users/gav/Repos/TestRepos/lab-web-test/keywords/lab/__lab_include.txt
Resource            /Users/gav/Repos/TestRepos/lab-web-test/keywords/notebook/__nb_include.txt
Resource            /Users/gav/Repos/TestRepos/lab-web-test/keywords/lab-addon/__lab_include.txt
Resource            /Users/gav/Repos/TestRepos/lab-web-test/keywords/id/__id_include.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/workspaces/__ws_include.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/identity/kw_id_common.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/identity/kw_idp_chooser.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/identity/vf_idp_chooser.txt
Resource            /Users/gav/Repos/TestRepos/shared-web-test/keywords/gdrive/__gd_include.txt
Variables           /Users/gav/Repos/TestRepos/slso-suite-test/libs/vf_slso_suite_env.py    ${webenv}    ${branch}    ${region}
Resource            /Users/gav/Repos/TestRepos/slso-suite-test/tests/__include_ui.txt


*** Variables ***
${ELEMENT}      /decide 
${URL1}         http://robotframework.org/robotframework/3.0.4/libraries/BuiltIn.html
${URL2}         https://robot-framework.readthedocs.io/en/latest/autodoc/robot.parsing.lexer.html#robot.parsing.lexer.tokens.Token
${URL3}         https://robotframework.org/Selenium2Library/Selenium2Library.html
${URL4}         https://confluence.smarttech.com/pages/viewpage.action?pageId=52762150
${1}            1
${2}            2
${3}            3

${ORLANDO}              https://orlando-dot-smart-suite-dev.appspot.com/login?feature=debug,entitlements,disable-marketing&env=dev
${CLASS_CODE}           18563
${lesson_name}          LESSON1


*** Keywords ***
Local: student - open browser and join a class
    [Arguments]    ${url}    ${class_code}    ${student_name}
    Open Browser    ${url}    ${browser}
    Set Window Size    1400    850
    LABC:SS Setup
    SLSO_SUITE: Wait for homepage to be loaded
    SLSO: Guest Student - Join class from home page
    SLSO: Guest Student - Verify New ClassCode Page
    SLSO: Guest Student - join a class    ${class_code}    ${student_name}
    Set Window Size    ${BROWSER_WIDTH}    ${BROWSER_HEIGHT}

*** Test Cases ***

How To Robot - Open a browser
    [Documentation]     Show how to open browswer, sleep and close browser
    ${browser_id}=    Selenium2Library.Open Browser        ${URL1}     gc
    # SeleniumLibrary.Press Keys   None    CTRL+T
    # sleep   1
    # Open Browser        ${URL3}     gc 
    sleep   3
    Selenium2Library.Close All Browsers

How To Robot - Create Lists/Dicts
    [Documentation]     Shows how to create a list or dict using the BuiltIt method. 
    # List 
    @{list1}=           Create List     1   2   3
    # Scalar List
    ${list2}=           Create List     a   b   c  
    # List
    ${list3}=           Create List     ${1}    ${2}    ${3}

How to Robot - If/Else
    [Documentation]     How to do an IF / ELSE to run a keyword. 
    Run Keyword if          5 == 5      Log To Console      5 == 5      
    ...                     ELSE        Log To Console      5 != 5

    Run Keyword Unless      5 == 5      Log To Console      5 == 5 so do't run keyword

How to Robot - Convert To Binary  
    [Documentation]     BuiltInMethod to convert number or character to Binary 
    :FOR    ${v}    IN      A     B     C     D     E
    \       ${conversion}=      Convert To Binary   ${v}    base=16
    \       Log     ${conversion}

    :FOR    ${v}    IN      24     56     12     201     198
    \       ${conversion}=      Convert To Binary   ${v}
    \       Log     ${conversion}


How to Robot - Continue For Loop If  
    [Documentation]
    :FOR    ${V}    IN      'A'   'B'   'C'  'D'   'E'
    \       Continue For Loop If    ${v}=='D'
    \       Log     ${v}

How to Robot - Convert to number or String
    [Documentation]     Variable numberes are represented as strings/unicode, this converts a string to a number and back.   
    ${num}      Set Variable    198.345  
    ${conversion}=    Convert To number   ${num}
    ${type1}    Evaluate    type($num)
    ${type2}    Evaluate    type($conversion)
    ${conversion2}=     Convert to string   ${conversion}
    ${type3}    Evaluate    type($conversion2)

How to Robot - Use Evaulate 
    [Documentation]     How to use the keyword Evaluate.
    ${ran}=     Evaluate   random.randint(0, 256)       modules=random


How to Robot - Use For Loops 
    [Documentation]     Examples of For loops 
    :FOR    ${v}    IN      1   2   3   4   5
    \       Run Keyword If  ${v}==4     Exit For Loop

    :FOR    ${v}    IN      6   7   8   9   10
    \       Exit For Loop If  ${v}==8

How to Robot - Get Length Keyword 
    [Documentation]     How to use the Get Length keyword   
    ${len}=     Get Length      What's the story morning glory


How to Robot - Get the time 
    [Documentation]     Get the time. 
    ${t}=   Get Time
    Log     ${t}    console=True

How to Robot - Keyword should exist
    [Documentation]     How to use the keyword should exist keyword
    Keyword Should Exist        Get Global Variables Count      msg=Override default fail messageord      

Get Robot Global Variable Count
    [Documentation]     Counts Global Variabls
    # Log Variables
    #[Teardown]  Close All Browsers 
    ${count}=    Get Global Variables Count
    Log     ${count} Variables Found    console=True

How to Robot - Run a keywork in PythonFiles
    [Documentation]    Uses the buitin method run_keyword(name, *args)
    ${browser_id}=    Selenium2Library.Open Browser        ${URL1}     gc
    sleep  3
    try_my_own_keyword      //*[@id="shortcuts-container s"]/div/a[46]
    sleep  5
    Log     Finished!


SLSO Test - Open Student Browsers
    [Documentation]    For Manual Testing Only!
    ...    Opens a number of browsers on a machine and signs in a student to the specified class as Student_${num}.
    ...    Note that opening many (20+) browsers on a single machine can bog the machine down so for more than 20 students
    ...     it is a good idea to run this script on multiple machines, hence the ${initial_student} variable.
    ...    Manual intervention needed for:
    ...    - confirming the student url
    ...    - entering the class code
    ...    - entering the initial student number
    ...    - entering the number of students (each opened in a new browser)
    ...    - resuming execution (which will close browsers)
    [Tags]    open_student_browsers
    ${url}=    Get Value From User    URL    ${SLSO_SUITE_URL}
    ${url}=    Convert To String    ${url}   # Python was crashing without this line.
    ${class_code}=    Get Value From User    Class Code
    ${initial_student}=    Get Value From User    First Student Number
    ${number_of_students}=    Get Value From User    Number Of Students
    ${limit}=   Evaluate    ${initial_student} + ${number_of_students}
    :FOR    ${num}    IN RANGE    ${initial_student}    ${limit}
    \    ${status}=    Run Keyword And Return Status    Local: student - open browser and join a class    ${ORLANDO}    ${CLASS_CODE}    Student_${num}
    Pause Execution
    [Teardown]    Close All Browsers

Joining String With Variables
    [Documentation]  Set variable and joining variables with strings. 
    ${cp_lesson_title}      Set Variable        //*[contains(@class, “title”) and text()=“${lesson_name}“]
    Log     ${cp_lesson_title}
    Log Variables

Log all variables 
    Log Variables  

Search Google For A Random Word 
    [Documentation]     Testing new keyword, what happens when you pass in an xpath that doesn't exist. 
    ${browser_id}=    Selenium2Library.Open Browser        https://www.google.es     gc
    ${ran}=     Get Random Word
    ${rand_speed}=  Get Random Num 
    Custom Input Text Controlled        //input[contains(@name, "q")]       ${ran}       ${rand_speed}
    # Custom Input Text Controlled          //input[contains(@name, 'no name')]   ShouldNotWork
    sleep   1
    Click Element   //input[contains(@value, "I'm Feeling Lucky")]
    sleep   5
    # Pause Execution     What did you get?

Subtract two numbers 
    Log             ${a_num}
    ${a_num}=       Evaluate    ${a_num} - ${1}
    Log             ${a_num}

Test Set Variable Keyword 
    ${idp}=     Set Variable If     ${SIGNINMS} == ${True}      microsoft       google 
    Log         ${idp}

Go To With Chrome Profile
    # Just put this here to save it. Not actually used in this file. 
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --allow-running-insecure-content
    Call Method    ${options}    add_argument    --disable-web-security
    Call Method    ${options}    add_argument    --user-data-dir\=/Users/gav/SLSO/Canada
    Create WebDriver    Chrome    chrome_options=${options}     executable_path=/Users/gav/SLSO/chromedriver
    Go To    https://stackoverflow.com

Test Setup With Chrome Profile
    # Set ${profile} variable
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --allow-running-insecure-content
    Call Method    ${options}    add_argument    --disable-web-security
    Call Method    ${options}    add_argument    --user-data-dir\=/Users/gav/SLSO/${profile}
    Create WebDriver    Chrome    chrome_options=${options}     executable_path=/Users/gav/SLSO/chromedriver
    Go To    ${SLSO_SUITE_LOGIN_PURCHASE_URL}
    Set Window Size    1400  800

Get ChromeDriver Path 
    ${var1}=    Set Variable    C:/webdriver/chromedriver
    ${var1}=    Set Variable If  '${OSRUN}' == 'mac'    /Users/gav/SLSO/chromedriver
    #[Return]    ${var1}

    #${list} =     Create List    --start-maximized    --disable-web-security
    #${args} =     Create Dictionary    args=${list}
    #${desired caps} =     Create Dictionary    platform=${OS}     chromeOptions=${args}
    #Open Browser    https://www.google.com    remote_url=${grid_url}    browser=${BROWSER}    desired_capabilities=${desired caps}

    