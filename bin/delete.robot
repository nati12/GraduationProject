*** Settings ***
Documentation      This robot file deletes all existing polls
Library            ../libs/VC_library.py
Suite Setup        Run Keywords
...                Open Browser
...                Open VibeCatch And Log In
Suite Teardown     Close Browser


*** Test Cases ***
Delete All
    Delete All
