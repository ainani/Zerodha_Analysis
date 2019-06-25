# WebDrivers exe paths

chrome_path = "chromedriver.exe"
firefox_path = "geckodriver.exe"
ie_path = "IEDriverServer.exe"

# To fetch WebDriver's path

def fetch_driver_path(browser_type):
    if browser_type == "Chrome":
        return chrome_path
    elif browser_type == "Firefox":
        return firefox_path
    else:
        return ie_path


# To fetch Login URL of Zerodha

def fetch_zerodha_url():
    url = "https://kite.zerodha.com/"
    return url

