*** Settings ***
Library  SeleniumLibrary
Variables  ../ObjectRepository/LoginLocators.py
#Variables  ../Variables/LoginDetails.py
Resource  ../Resources/HoldingsScreenshot.robot

*** Variables ***

*** Test Cases ***
TC001 Validate login and save the Holdings screenshot
    [Documentation]  This test case will login to Zerodha and save Holdings screenshot
    [Tags]  Login
    Login to Zerodha
    Click on Holdings

TC002 Validate the Scrips
    Validate the scrips

TC003 Close Browser
    close browser