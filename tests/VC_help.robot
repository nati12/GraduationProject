*** Settings ***
Documentation      This test suite tests help options on Vibecatch website.
Library            ../libs/VC_library.py
Variables          ../libs/variables.py
Suite Setup        Open Browser        ${BROWSER}
Test Setup         Open VibeCatch And Log In
Suite Teardown     Close Browser


*** Test Cases ***
Open Frequently Asked Questions
    Choose From Help Options    ${FAQ}
    FAQ Page Should Be Open

Open Poll Tutorial
    Choose From Help Options    ${TUTORIAL}
    Poll Tutorial Should Be Open

Open QWL Playground
    Choose From Help Options    ${QWL_PLAYGROUND}
    QWL Playground Should Be Open
