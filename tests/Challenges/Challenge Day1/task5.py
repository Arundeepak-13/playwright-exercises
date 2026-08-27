from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://practicesoftwaretesting.com/')
    print('Application opened')




    #Valid credentials-Login succeeds
    page.get_by_text('Sign in').click()
    print('Login page opened')
    email = page.wait_for_selector('[data-test="email"]')
    password = page.wait_for_selector('[data-test="password"]')
    login_button = page.wait_for_selector('[data-test="login-submit"]')
    email.fill('deepakvb01@gmail.com')
    password.fill('kP9#vX2!mL7$qR5*')
    login_button.click()
    page.wait_for_timeout(3000)
    print('Current URL:', page.url)
    assert '/login' not in page.url
    print('Valid login test passed')




    #Invalid password - Login fails
    page = browser.new_page()
    page.goto('https://practicesoftwaretesting.com/')
    page.get_by_text('Sign in').click()
    email = page.wait_for_selector('[data-test="email"]')
    password = page.wait_for_selector('[data-test="password"]')
    login_button = page.wait_for_selector('[data-test="login-submit"]')
    email.fill('deepakvb01@gmail.com')
    password.fill('WrongPassword123')
    login_button.click()
    page.wait_for_timeout(2000)
    print('Current URL:', page.url)
    assert '/login' in page.url
    print('Invalid password test passed')    



    #Invalid Email - Fails
    page = browser.new_page()
    page.goto('https://practicesoftwaretesting.com/')
    page.get_by_text('Sign in').click()
    email = page.wait_for_selector('[data-test="email"]')
    password = page.wait_for_selector('[data-test="password"]')
    login_button = page.wait_for_selector('[data-test="login-submit"]')
    email.fill('invaliduser123456@gmail.com')
    password.fill('Password123')
    login_button.click()
    page.wait_for_timeout(2000)
    print('Current URL:', page.url)
    assert '/login' in page.url
    print('Invalid email test passed')




    #Empty credentials - Validation/error displayedS
    page = browser.new_page()
    page.goto('https://practicesoftwaretesting.com/')
    page.get_by_text('Sign in').click()
    login_button = page.wait_for_selector('[data-test="login-submit"]')
    login_button.click()
    page.wait_for_timeout(1000)
    print('Empty credentials validation:')
    print(page.locator('body').inner_text())
    print('Empty credentials test completed')


    browser.close()

