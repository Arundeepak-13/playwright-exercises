from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto('https://practicesoftwaretesting.com/')
    print('Chrome Successfully Opened')

    # Select Product
    product = page.wait_for_selector('.card')
    print("Products are displayed")
    product.click()
    print('Product Selected')



    # Verify Product Name
    product_name = page.wait_for_selector("h1")
    assert product_name.is_visible()
    product_name_text = product_name.inner_text().strip()
    print("Product name:", product_name_text)
    print("Product name is displayed")



    # Verify Product Price
    product_price = page.wait_for_selector("[data-test='unit-price']")
    assert product_price.is_visible()
    product_price_text = product_price.inner_text().strip()
    print("Product price:", product_price_text)
    print("Product price is displayed")



    # Verify Product Image
    product_image = page.wait_for_selector("img")
    assert product_image.is_visible()
    print("Product image is displayed")



    # Verify Product Description
    product_description = page.wait_for_selector("[data-test='product-description']")
    assert product_description.is_visible()
    print("Product description:", product_description.inner_text())



    # Verify Product Quantity
    quantity = page.wait_for_selector("[data-test='quantity']")
    assert quantity.is_visible()
    print("Product quantity control is displayed")
    page.wait_for_timeout(1000)


    # Verify Add to Cart Button
    add_to_cart = page.wait_for_selector("[data-test='add-to-cart']")
    assert add_to_cart.is_visible()
    print("Add to Cart button is visible")
    page.wait_for_timeout(1000)



    # Add Product to the cart 
    add_to_cart.click()
    print("Product added to cart")



    # Navigate to the cart
    cart = page.wait_for_selector('[aria-label="cart"]')
    cart.click()
    print("Cart opened")


  
    # Verify Product Name in the Cart
    cart_product = page.wait_for_selector('[data-test="product-title"]')
    assert cart_product.is_visible()
    cart_product_name = cart_product.inner_text().strip()
    print("Cart product:", cart_product_name)
    assert cart_product_name == product_name_text
    print("Product name matches in cart")



    # Verify Product Price in the Cart
    cart_price = page.wait_for_selector('[data-test="product-price"]')
    assert cart_price.is_visible()
    cart_price_text = cart_price.inner_text().strip()
    print("Cart price:", cart_price_text)



    # Remove $ symbol before comparing
    cart_price_value = cart_price_text.replace("$", "").strip()
    assert cart_price_value == product_price_text
    print("Product price matches in cart")
    page.wait_for_timeout(1000)



    browser.close()