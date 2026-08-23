from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://practicesoftwaretesting.com/")
    print("Chrome Successfully Opened")

    #productA
    search = page.wait_for_selector("[placeholder='Search']")
    search.fill("Combination Pliers")
    search_button = page.get_by_role("button", name="Search")
    search_button.click()
    page.wait_for_timeout(2000)


    #  verfiy  productA selected
    product_a = page.locator("[data-test='product-name']").filter(has_text="Combination Pliers")
    assert product_a.is_visible()
    print("Product A is displayed")
    product_a.click()
    print("Product A selected")


    # Product A Price
    product_a_price = page.wait_for_selector("[data-test='unit-price']")
    assert product_a_price.is_visible()
    product_a_price_value = product_a_price.inner_text()
    print("Product A price:", product_a_price_value)



    # Add Product A
    add_to_cart = page.wait_for_selector("[data-test='add-to-cart']")
    assert add_to_cart.is_visible()
    add_to_cart.click()
    print("Product A added to cart")
    page.wait_for_timeout(1000)



    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_timeout(2000)


    #productB
    search = page.wait_for_selector("[placeholder='Search']")
    search.fill("Bolt Cutters")
    search_button = page.get_by_role("button", name="Search")
    search_button.click()
    page.wait_for_timeout(2000)


    #verify product B selected
    product_b = page.locator("[data-test='product-name']").filter(has_text="Bolt Cutters")
    assert product_b.is_visible()
    print("Product B is displayed")
    product_b.click()
    print("Product B selected")



    # Product B Price
    product_b_price = page.wait_for_selector("[data-test='unit-price']")
    assert product_b_price.is_visible()
    product_b_price_value = product_b_price.inner_text()
    print("Product B price:", product_b_price_value)


    # Add Product B
    add_to_cart = page.wait_for_selector("[data-test='add-to-cart']")
    assert add_to_cart.is_visible()
    add_to_cart.click()
    print("Product B added to cart")
    page.wait_for_timeout(1000)




    # Open Cart
    cart = page.wait_for_selector('[aria-label="cart"]')
    assert cart.is_visible()
    cart.click()
    print("Cart opened")
    page.wait_for_timeout(2000)


  
    # Verify Product A
    product_a_cart = page.locator("tbody").get_by_text("Combination Pliers",exact=True)
    assert product_a_cart.is_visible()
    print("Product A is available in cart")



    # Verify Product B
    product_b_cart = page.locator("tbody").get_by_text("Bolt Cutters",exact=True)
    assert product_b_cart.is_visible()
    print("Product B is available in cart")



    # Product A Row
    product_a_row = page.locator("tbody tr").filter(has_text="Combination Pliers")
    print("Product A row found")



    # Product B Row
    product_b_row = page.locator("tbody tr").filter(has_text="Bolt Cutters")
    print("Product B row found")


    # Verify Product A Quantity
    product_a_quantity = product_a_row.locator("input")
    assert product_a_quantity.is_visible()
    print("Product A quantity:",product_a_quantity.input_value())
    assert product_a_quantity.input_value() == "1"
    print("Product A quantity is correct")



    # Verify Product B Quantity
    product_b_quantity = product_b_row.locator("input")
    assert product_b_quantity.is_visible()
    print("Product B quantity:",product_b_quantity.input_value())
    assert product_b_quantity.input_value() == "1"
    print("Product B quantity is correct")



    # Verify Product A Price
    product_a_cart_price = product_a_row.locator("[data-test='product-price']")
    assert product_a_cart_price.is_visible()
    print("Product A cart price:",product_a_cart_price.inner_text())
    assert (product_a_cart_price.inner_text()== "$" + product_a_price_value)
    print("Product A price is correct")



    # Verify Product B Price
    product_b_cart_price = product_b_row.locator("[data-test='product-price']")
    assert product_b_cart_price.is_visible()
    print("Product B cart price:",product_b_cart_price.inner_text())
    assert (product_b_cart_price.inner_text()== "$" + product_b_price_value)
    print("Product B price is correct")



    # Remove Product A
    remove_product_a = product_a_row.locator("a").last
    assert remove_product_a.is_visible()
    remove_product_a.click()
    print("Product A removed")
    page.wait_for_timeout(2000)



    # Verify Product A Removed
    product_a_after_remove = page.locator("tbody").get_by_text("Combination Pliers",exact=True)
    assert not product_a_after_remove.is_visible()
    print("Product A is removed from cart")



    # Verify Product B Remains
    product_b_after_remove = page.locator("tbody").get_by_text("Bolt Cutters",exact=True)
    assert product_b_after_remove.is_visible()
    print("Product B remains in cart")



    page.wait_for_timeout(3000)
    browser.close()