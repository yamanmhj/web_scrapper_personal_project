import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service

def Add_driver(website):
    print("launching chrome browser...")
    chrome_driver_path = './chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(chrome_driver_path),options=options)

    try:
        driver.get(website)
        print("Page Loaded")
        html = driver.page_source
        return html
    finally:
        driver.quit()
