*** Settings ***
Documentation      This robot file deletes all existing polls
Library            ../libs/library.py
Suite Setup        Run Keywords
...                Open Browser
...                Open Page And Log In
Suite Teardown     Close Browser


*** Test Cases ***
Delete All
    Delete All
