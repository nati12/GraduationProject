*** Settings ***
Documentation      This test suite tests help options on the website.
Library            ../libs/library.py
Variables          ../libs/variables.py
Suite Setup        Open Browser        ${BROWSER}
Test Setup         Open Page And Log In
Suite Teardown     Close Browser


*** Test Cases ***
Open Frequently Asked Questions
    Choose From Help Options    ${FAQ}
    FAQ Page Should Be Open

Open Poll Tutorial
    Choose From Help Options    ${TUTORIAL}
    Poll Tutorial Should Be Open

Open A Playground
    Choose From Help Options    ${A_PLAYGROUND}
    A Playground Should Be Open
