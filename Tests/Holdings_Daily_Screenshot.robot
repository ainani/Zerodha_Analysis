*** Settings ***
#Resource  ../Resources/Common.robot
Variables  ../ObjectRepository/LoginLocators.py
Variables  ../Variables/LoginDetails.py
Library  SeleniumLibrary


*** Variables ***

*** Test Cases ***
Login to Zerodha
    [Documentation]  This test case will login to Zerodha successfuly
    [Tags]  Login
    open browser  ${url}  ${browser_type}
    Wait until page contains  Login to Kite
    Input Text  ${zr_username}  ${username}
    Input Text  ${zr_password}  ${password}
    Click Button  ${zr_submit}
    wait until page contains  PIN
    Input Text  ${zr_pin}  ${pin}
    Click Button  ${zr_pin_continue}
    Wait Until Page Contains  ${name}
    Page Should Contain  Hi, ${name}
    Click Link  Holdings
    Set Screenshot Directory  ${holdings_dir}
    Capture Page Screenshot  ${holdings_dir}/holdings.png
    sleep  5s
    Close Browser



*** Keywords ***
