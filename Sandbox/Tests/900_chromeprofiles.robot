*** Settings ***
Library             LumioLibrary
Library             Selenium2Library
Library             Screenshot
Force Tags          purchase_smoke      profiles_chrome
Test Teardown       Custom Teardown

*** Variables ***  
${test_account}     gavinmcguigan.teacher@smartwizardschool.com
${test_account2}     gavinmcguigan.student1@smartwizardschool.com
${test_account3}     gavinmcguigan.student2@smartwizardschool.com
${test_account4}     slso.purchase.ca@smartwizardschool.com
${test_account5}      slso.purchase.uk@smartwizardschool.com
${test_account6}     slso.purchase.us@smartwizardschool.com
${test_account7}     slso.purchase.aus@smartwizardschool.com

${pass}              wizard123!

*** Test Cases ***
Chrome Profile UAT
    Open Chrome Profile     https://suite.smarttech-uat.com/library
    
Chrome Profile DEV
    Open Chrome Profile     https://suite.smarttech-dev.com/library
    
Chrome Profile PROD
    Open Chrome Profile     https://suite.smarttech-prod.com/library


Check Console Logs 
    Open Chrome Profile     https://suite.smarttech-dev.com/library?feature=debug,test-mixpanel-tracking,group-ungroup
    Get Browser Log
    [Teardown]  Close Browser


*** Keywords ***
Open Chrome Profile
    [Arguments]         ${url}  
    ${options_and_desiredcapabilites}=         Download Chrome Profile     ${test_account}
    Create WebDriver    Chrome    chrome_options=${options_and_desiredcapabilites[0]}     desired_capabilities=${options_and_desiredcapabilites[1]}
    Profile Login Teacher       ${test_account}     ${pass}      ${url}    
    
Custom Teardown
    Run Keyword If Test Failed  Capture Page Screenshot
    Close All Browsers
    Run Keyword If Test Passed  Upload Chrome Profile    ${test_account}