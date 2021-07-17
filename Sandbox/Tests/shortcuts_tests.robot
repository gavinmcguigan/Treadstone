Library             ${CURDIR}/../libs/ChromeProfileLib
Library             Selenium2Library
Library             Screenshot
Force Tags          purchase_smoke
Test Teardown       Custom Teardown

*** Variables ***  
${test_account}     gavinmcguigan.teacher@smartwizardschool.com
${lib_url}          https://suite.smarttech-dev.com/library

*** Test Cases ***
Chrome Profile DEV
    Open Chrome Profile     ${lib_url}
    


*** Keywords ***
Open Chrome Profile
    [Arguments]         ${url}  
    ${options}=         Download Chrome Profile     ${test_account}
    Create WebDriver    Chrome    chrome_options=${options}
    Profile Login       ${test_account}      ${url}    
    
Custom Teardown
    Run Keyword If Test Failed  Capture Page Screenshot
    Close All Browsers
    Run Keyword If Test Passed  Upload Chrome Profile    ${test_account}