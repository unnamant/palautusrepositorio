*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  kaitsu
    Set Password  kaitsunen123
    Set password confirmation  kaitsunen123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ka
    Set Password  kalle456
    Set password confirmation  kalle456
    Click Button  Register
    Register Should Fail With Message  Username must be at least 3 characters long


Register With Valid Username And Too Short Password
    Set Username  kaitsu
    Set Password  kaits1
    Set password confirmation  kaits1
    Click Button  Register
    Register Should Fail With Message  Password must be atleast 8 characters long


Register With Valid Username And Invalid Password
    Set Username  kaitsu
    Set Password  kallelainen
    Set password confirmation  kallelainen
    Click Button  Register
    Register Should Fail With Message  Password cannot consist only of letters


Register With Nonmatching Password And Password Confirmation
    Set Username  kaitsu
    Set Password  kallelainen
    Set password confirmation  kallelanen
    Click Button  Register
    Register Should Fail With Message  Passwords don't match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle456
    Set password confirmation  kalle456
    Click Button  Register
    Register Should Fail With Message  Username already taken

*** Keywords ***
Register Should Succeed
    Main Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page
