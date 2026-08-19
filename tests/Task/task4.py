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

  
    product_name = page.wait_for_selector("h1").inner_text()
    print("Product name:", product_name)

  
    product_price = page.wait_for_selector("[data-test='unit-price']").inner_text()
    print("Product price:", product_price)


    add_to_cart = page.wait_for_selector("[data-test='add-to-cart']")
    assert add_to_cart.is_visible()
    print("Add to Cart button is visible")

    add_to_cart.click()
    print("Product added to cart")

  
    cart = page.wait_for_selector('[aria-label="cart"]')
    assert cart.is_visible()

    cart.click()
    print("Cart opened")

  
    cart_product = page.wait_for_selector('[data-test="product-title"]')

    assert product_name in cart_product.inner_text()
    print("Product verified in cart")


    quantity = page.wait_for_selector('[data-test="product-quantity"]')
    assert quantity.input_value() == "1"
    print("Quantity verified:", quantity.input_value())


    cart_price = page.wait_for_selector('[data-test="product-price"]')
    assert product_price in cart_price.inner_text()
    print("Price verified:", cart_price.inner_text())

    remove_product = page.wait_for_selector('[data-icon="xmark"]')
    assert remove_product.is_visible()
    remove_product.click()
    print("Product Removed")


    page.wait_for_timeout(5000)


