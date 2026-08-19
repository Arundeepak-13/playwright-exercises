from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://practicesoftwaretesting.com/')
    print('Chrome Successfully Opened')

    product = page.wait_for_selector(".card")
    print("Product is displayed")

    product.click()
    print("Product selected")    

    product_name = page.wait_for_selector("h1")
    assert product_name.is_visible()
    print("Product name:", product_name.inner_text())

    add_to_cart = page.wait_for_selector("[data-test='add-to-cart']")
    assert add_to_cart.is_visible()
    print("Add to Cart button is visible")

    add_to_cart.click()
    print("Product added to cart")

    cart = page.wait_for_selector('[aria-label="cart"]')
    assert cart.is_visible()
    cart.click()
    print("Cart opened")   


    page.wait_for_timeout(3000)




