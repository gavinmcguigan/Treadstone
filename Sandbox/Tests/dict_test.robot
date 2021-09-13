*** Settings ***
Library         LumioLib


*** Variables ***
${ov_header}=    {"$time": "123123123"}

*** Test Cases ***
First Test 
    Run Keyword If   "{ov_header}" != "${EMPTY}"    Log  ${ov_header}
    Run Keyword If   "{ov_header}" == "${EMPTY}"    Log  EMPTY  
    &{dict}=    Create Dictionary       key=time    value=123123123
    Log     ${dict}

    ${value}=  Get From Dictionary      ${time}     

    ${time}=  Get Time   123123123
    Log     ${time}


Second Test
    Test Keyword