from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")


    #X-Path - Relative xpath "//"
    #Using attribute - //tagname[@attributename = "value"]

    username = page.wait_for_selector('//input[@name="username"]')
    username.type('Admin')
    password = page.wait_for_selector('//input[@placeholder="Password"]')
    password.type('admin123')
    login = page.wait_for_selector('//button[@type="submit"]')
    login.click()
    page.wait_for_timeout(3000)
