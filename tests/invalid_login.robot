*** Settings ***
Documentation      This test suite tests invalid logins using DataDriver in the web page
...                website.
Library            ../libs/library.py
Library            DataDriver            file=../data/invalid_login.xlsx
Variables          ../libs/variables.py
Suite Setup        Open Browser        ${BROWSER}
Test Setup         Open Login
Suite Teardown     Close Browser
Test Template      Invalid logins


*** Test Cases ***
Login with invalid credentials


*** Keywords ***
Invalid Logins
    [Arguments]          ${username}    ${password}
    Login Should Fail    ${username}    ${password}
