*** Settings ***
Library           BuiltIn
Library           SeleniumLibrary
Library           String
Variables  ../ObjectRepository/LoginLocators.py
Variables  ../Variables/LoginDetails.py
Variables  ../Variables/Scrips.py

*** Keywords ***

Click on Holdings
    Click Link  Holdings
    Set Screenshot Directory  ${holdings_dir}
    Capture Page Screenshot  ${holdings_dir}/holdings.png
    sleep  5s

Validate the scrips
    ${scrips_cnt}  get text  //div/section[1]/header[1]/h3[1]/span[2]
    ${scrips_cnt}  remove string  ${scrips_cnt}  (  ,  )
    log  ${scrips_cnt}
    :FOR  ${i}  IN RANGE  1  ${scrips_cnt} + 1
    \   ${symbol}  get text  //tr[${i}]/td[1]/span[1]
    \   ${qty}  get text  //tr[${i}]/td[2]
    \   ${avg}  get text  //tr[${i}]/td[3]
    \   ${ltp}  get text  //tr[${i}]/td[4]
