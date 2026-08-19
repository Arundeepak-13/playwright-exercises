from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://practicesoftwaretesting.com/')
    print('chrome Successfully Opened')


    product = page.wait_for_selector('.card')
    print("product are displayed")

    product.click()
    print('product Selected')

    product_name = page.wait_for_selector("h1")
    assert product_name.is_visible()
    print("Product name:", product_name.inner_text())

    product_price = page.wait_for_selector("[data-test='unit-price']")
    assert product_price.is_visible()
    print("Product price:", product_price.inner_text())

    product_image = page.wait_for_selector("img")
    assert product_image.is_visible()
    print("Product image is displayed")

    product_description = page.wait_for_selector("[data-test='product-description']")
    assert product_description.is_visible()
    print("Product description:", product_description.inner_text())


    #add to cart

    add_to_cart = page.wait_for_selector("[data-test='add-to-cart']")
    assert add_to_cart.is_visible()
    print("Add to Cart button is visible")

    add_to_cart.click()
    print("Product added to cart")

    cart = page.wait_for_selector('[aria-label="cart"]')
    cart.click()
    print("Cart opened")

    cart_product = page.wait_for_selector('[data-test="product-title"]')
    assert cart_product.is_visible()
    print("Product is available in cart")
    
       
    page.wait_for_timeout(3000)