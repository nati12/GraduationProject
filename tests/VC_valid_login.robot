*** Settings ***
Documentation      This test suite tests valid login functions in VibeCatch
...                website.
Library            ../libs/VC_library.py
Variables          ../libs/variables.py
Suite Setup        Open Browser        ${BROWSER}
Test Setup         Open Login
Suite Teardown     Close Browser


*** Test Cases ***
Valid login And Log Out
    Submit Credentials    ${VALID_USERNAME}    ${VALID_PASSWORD}
    Login Should Succeed
    Log Out
