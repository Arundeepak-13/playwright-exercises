from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://practicesoftwaretesting.com/')
    print('Chrome Successfully Opened')

    print(page.title())
    print('Page title verified')

    navigation = page.wait_for_selector('nav')
    assert navigation.is_visible()
    print('Navigation is visible')

    products = page.locator('.card')
    assert products.count() > 0
    print('Products are displayed')


    page.get_by_text('Combination Pliers').click()
    print('Product selected')
    page.wait_for_timeout(3000)