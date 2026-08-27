from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://practicesoftwaretesting.com/')
    print('chrome Successfully Opened')

  
    searchbox = page.wait_for_selector('#search-query')
    searchbox.fill('Pliers')

    searchbutton = page.wait_for_selector('button[type="submit"]')
    searchbutton.click()

    resultcount = page.wait_for_selector(
        '[data-testid="search-result-count"]'
        )
    print(resultcount.inner_text())

    assert resultcount.is_visible()
    assert 'pliers' in resultcount.inner_text().lower()
    print('Search result verified successfully')


    searchbox.fill('deepak')
    searchbutton.click()

    page.wait_for_timeout(3000)

    resultcount = page.wait_for_selector(
    '[data-testid="search-result-count"]'
    )
    print(resultcount.inner_text())
    assert "0 products found for 'deepak'" in resultcount.inner_text().lower()
    print('No-result search verified successfully')
  


    



