*** Settings ***
Documentation      This test suite tests creating custom polls in the web page.
Library            ../libs/library.py
Variables          ../libs/variables.py
Suite Setup        Open Browser        ${BROWSER}
Test Setup         Open Page And Log In
Suite Teardown     Close Browser


*** Test Cases ***
Create custom poll
    Create New Custom Poll
    Poll Should Exist
    Add New Question
    Delete Poll
    Poll Should Not Exist
