*** Settings *** 
Resource            ${CURDIR}/../../../slso-suite-test/tests/__include_ui.txt

*** Test Cases ***
Get Auth Cookies For Purchase Tests
    [Template]  Get Auth Cookies For User
        ${slso_purchase_ca}    ${slso_user_password}
        ${slso_purchase_us}    ${slso_user_password}
        ${slso_purchase_uk}    ${slso_user_password}
        ${slso_purchase_aus}   ${slso_user_password}

*** Keywords ***
Get Auth Cookies For User
    [Arguments]    ${user}    ${pwd}
    SLSO_SUITE: Open Browser To home Page
    Run Keyword And Continue On Failure    SLSO: Log Into Lessons Page    ${user}    ${pwd}
    [Teardown]    Close Browser