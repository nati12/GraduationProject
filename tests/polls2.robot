*** Settings ***
Documentation      This test suite tests creating polls in the web page,
...                changing name and viewing results or sending a reminder.
Library            ../libs/library.py
Variables          ../libs/variables.py
Suite Setup        Open Browser        ${BROWSER}
Test Setup         Open Page And Log In
Suite Teardown     Close Browser


*** Test Cases ***
Create Poll and Change Name
    Create New Poll
    Poll Should Exist
    Change Name
    Delete Poll
    Poll Should Not Exist

Create Poll In Finnish And Send
    [Documentation]        Sends created poll to teantestaus@gmail.com.
    ...                    Settings: translated to Finnish
    Create New Poll
    Poll Should Exist
    Add Email
    Translate To Finnish
    Send Feedback Request Now
    Email Should Be Sent
    Delete Poll
    Poll Should Not Exist


View Results
    Poll Should Exist                        test1
    View Results Or Send Reminder            test1
