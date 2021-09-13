*** Settings ***
Test Setup      Local - Test Setup
Test Teardown   Local - Test Teardown 


*** Test Cases ***
First Test
    Log To Console      _
    Log To Console      First Test: Step 1.1
    Sleep  1
    Log To Console      First Test: Step 1.2
    Sleep  1
    Log To Console      First Test: Step 1.3
    Sleep  1
    Log To Console      First Test: Step 1.4
    Sleep  1
    Log To Console      First Test: Step 1.5 

Second Test
    Log To Console      _
    Log To Console      Second Test: Step 2.1
    Sleep  1
    Log To Console      Second Test: Step 2.2
    Sleep  1
    Log To Console      Second Test: Step 2.3
    Sleep  1
    Log To Console      Second Test: Step 2.4
    Sleep  1
    Log To Console      Second Test: Step 2.5 


*** Keywords ***
Local - Test Setup
    Log To Console      _
    Log To Console      Test Setup: Running Test Setup
    Sleep  1  
    Log To Console      Test Setup: Check we're at the library 
    Sleep  1
    Log To Console      Test Setup: Delete all lessons 
    Sleep  1 
    Log To Console      Test Setup: Last step in setup
    Fail 
     

Local - Test Teardown 
    Log To Console      _
    Run Keyword If Test Failed      Log To Console   Test Teardown: Test Failed 
    Run Keyword If Test Passed      Log To Console   Test Teardown: Test Passed 

## Scenarios 

# Test setup fails
# ...  Test should not run
# Test teardown will run and therefore always try to delete the lessons - this is NOT okay

# Test setup passes
# ... Test can pass or fail
# Test teardown will run and therefore always try to delete the lessons - this is okay


# The problem with run keyword if test failed/passed, is that it can pass the setup and fail the test
# ...  under these circumstance, we do want to run delete all lessons.