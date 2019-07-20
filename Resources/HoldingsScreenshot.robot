*** Settings ***
Library           BuiltIn
Library           SeleniumLibrary
Variables  ../ObjectRepository/LoginLocators.py
Variables  ../Variables/LoginDetails.py
Variables  ../Variables/Scrips.py

*** Keywords ***

Login to Zerodha
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

Click on Holdings
    Click Link  Holdings
    Set Screenshot Directory  ${holdings_dir}
    Capture Page Screenshot  ${holdings_dir}/holdings.png
    sleep  5s

#Validate the scrips
    ${symbol}  get text  //tr[1]/td[1]/span[1]
    #${text}  get text  //span[contains(.,'${scrips}[0]')]
    ${qty}  get text  //tr[1]/td[2]
    #${text1}  get text  //td[@class='right']//span
    ${avg}  get text  //tr[1]/td[3]
    ${ltp}  get text  //tr[1]/td[4]
    #should contain  ${text}  AMARAJABAT


Validate the scrips
    :FOR  ${i}  IN RANGE  1  13
    \   ${symbol}  get text  //tr[${i}]/td[1]/span[1]
    \   ${qty}  get text  //tr[${i}]/td[2]
    \   ${avg}  get text  //tr[${i}]/td[3]
    \   ${ltp}  get text  //tr[${i}]/td[4]
