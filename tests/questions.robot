*** Settings ***
Documentation      This test suite contains tests for adjusting
...                number of questions in the created poll.
Library            ../libs/library.py
Variables          ../libs/variables.py
Suite Setup        Run Keywords
...                Open Browser     ${BROWSER}    AND
...                Open Page And Log In      AND
...                Create New Poll
Test Template      Number Of Questions Should Match
Suite Teardown     Run Keywords
...                Go To Home Page
...                Delete Poll
...                Close Browser


*** Test Cases ***
Three Questions       3
Six Questions         6
Nine Questions        9
Twelve Questions      12
All Questions         15


*** Keywords ***
Number Of Questions Should Match
    [Arguments]    ${num}
    Adjust Number Of Questions    ${num}
    Check Poll Form               ${num}
