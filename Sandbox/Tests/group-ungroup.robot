*** Settings ***
Library         Shortcuts
Library         LumioLibrary
Library         Selenium2Library
Library         Screenshot
Resource        ${CURDIR}/../../../slso-suite-test/tests/__include_ui.txt

Force Tags      purchase_smoke      profiles_chrome

*** Variables ***
${test_account}     gavinmcguigan.teacher@smartwizardschool.com

*** Test Cases ***
Grouping Annotations 
    Log To Console          Starting First Group Test. 
    Local: Open Chrome Profile     

    Local: Show Annotation Type Count

    #Start Recording The Console 
    #Check For Event In Console Log      Mixpanel event Teacher: Page template added sent
    sleep  20
    [Teardown]  Close Browser 


*** Keywords ***
Local: Open Chrome Profile
    [Arguments]
    ${options_and_desiredcapabilites}=         Download Chrome Profile     ${test_account}
    Create WebDriver    Chrome    chrome_options=${options_and_desiredcapabilites[0]}     desired_capabilities=${options_and_desiredcapabilites[1]}
    Profile Login Teacher       ${test_account}     wizard123!      https://suite.smarttech-dev.com/library?feature=debug,test-mixpanel-tracking,group-ungroup    
    Go To      https://suite-story136627.smarttech-uat.com/edit/16da126a-34a7-40b1-a780-ad7e5799c33f/01d0d70c-19d2-7eb5-c2d3-d3c4d3c47638?feature=debug,test-mixpanel-tracking,group-ungroup 
    Wait Until Page Contains Element        //p[contains(text(), 'Finish Editing')]     120 
    Sleep    20                                                          

Local: Show Annotation Type Count
    ${annotation_count}=    Execute Javascript  ${CURDIR}/../Libs/JavaScript/getGroupCount.js 
    Log To Console     Total Annotations: ${annotation_count[0]}
    Log To Console     Groups: ${annotation_count[1]}    
    Log To Console     NonGroups: ${annotation_count[2]}
    Log To Console     Cloners: ${annotation_count[3]}
    Log To Concoe      Locked Annotations: ${annotation_count[4]}
