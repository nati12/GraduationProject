*** Settings ***
Documentation      This test suite tests creating polls in the 
...                website with different settings and viewing results or sending a reminder.
Library            ../libs/library.py
Variables          ../libs/variables.py
Suite Setup        Open Browser        ${BROWSER}
Test Setup         Open Page And Log In
Suite Teardown     Close Browser


*** Test Cases ***
Create Poll And Delete It
    Create New Poll
    Poll Should Exist
    Delete Poll
    Poll Should Not Exist

Create Poll With Invalid Name
    Create Poll With Empty Namefield
    Creating Poll Should Fail

Create Poll And Schedule Sending
    [Documentation]        Schedules sending created poll to teantestaus@gmail.com.
    ...                    Settings: Streamlined, email daily 12PM.
    Create New Poll
    Poll Should Exist
    Make Streamlined
    Schedule Sending Email
    Email Should Be Scheduled
    Delete Poll
    Poll Should Not Exist

Create Poll and Change Name
    Create New Poll
    Poll Should Exist
    Change Name
    Delete Poll
    Poll Should Not Exist

Create Poll And Use It As A Template
    Create New Poll
    Poll Should Exist
    Mark As A Template
    Poll Should Be Template
    Create New Poll Using Template
    Poll Should Exist         ${NEW_POLL_NAME}
    Delete Poll
    Poll Should Not Exist
    Delete Poll               ${NEW_POLL_NAME}
    Poll Should Not Exist     ${NEW_POLL_NAME}
