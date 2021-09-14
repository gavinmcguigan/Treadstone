*** Settings ***
Library             SeleniumLibrary 


*** Test Cases ***
First Test 
    Open Browser    http://www.google.es    Chrome
    Sleep   5
    Close All Browsers