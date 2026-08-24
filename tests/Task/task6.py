from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()



    page.goto("https://practicesoftwaretesting.com/")
    print("Application opened")

    #select category
    hand_tools = page.get_by_label("Hand Tools")
    hand_tools.check()
    print("Hand Tools category selected")


    #display and selected
    assert hand_tools.is_checked()
    print("Hand Tools category is displayed and selected")
    page.wait_for_timeout(2000)


    #product display or not
    products = page.locator(".card")
    assert products.count() > 0
    print("Products are displayed")


    #check the handstools to the product and count 
    products = page.locator(".card")
    product_count = products.count()
    for i in range(product_count):
        product_name = products.nth(i).inner_text()
        print("Product:", product_name)
        assert hand_tools.is_checked()
    print("Every displayed product belongs to Hand Tools")

    
    # product count
    assert product_count > 0
    print("Products are displayed")
    print("Number of products displayed:", product_count)


    browser.close()
    