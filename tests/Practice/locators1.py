from playwright.sync_api import sync_playwright

with sync_playwright() as play:
    browser = play.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    #CSSSelector - id - # , class - , attribute 
    #id using
    #https://demo.automationtesting.in/Index.html
    # emailtxtbox = page.wait_for_selector('#email')
    # emailtxtbox.type('test@gmail.com')
    # buttonlogin = page.wait_for_selector('#enterimg')
    # buttonlogin.click()
    # page.wait_for_timeout(3000)



    #tagname[attribute = "vaule"]
    username = page.wait_for_selector('input[name="username"]')
    username.type('Admin')
    password = page.wait_for_selector('input[type="password"]')
    password.type('admin123')
    loginbutton = page.wait_for_selector('button[type="submit"]')
    loginbutton.click()
    page.wait_for_timeout(3000)

