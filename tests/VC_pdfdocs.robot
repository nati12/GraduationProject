*** Settings ***
Documentation      This test suite tests access to customer guide PDF documents on Vibecatch
...                website. Data for test cases is collected from a separate file using DataDriver.
Library            ../libs/VC_library.py
Library            DataDriver        file=../data/pdf_docs.xlsx
Variables          ../libs/variables.py
Suite Setup        Run Keywords
...                Open Browser    ${BROWSER}    AND
...                Open VibeCatch And Log In
Test Template      Download And Check PDF Document
Suite Teardown     Close Browser


*** Test Cases ***
Download PDF Document


*** Keywords ***
Download And Check PDF Document
    [Arguments]    ${doc_name}    ${text}    ${pages}
    Choose PDF Document        ${doc_name}
    Download And Check PDF     ${text}    ${pages}
    [Teardown]    Remove PDF
