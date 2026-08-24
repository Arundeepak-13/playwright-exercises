from playwright.sync_api import sync_playwright, expect


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # SCENARIO 1 - VALID CHECKOUT
    print("Scenario 1 - Valid Checkout")
    page.goto("https://practicesoftwaretesting.com/")


    # Search product
    page.locator('[data-test="search-query"]').fill("Combination Pliers")
    page.locator('[data-test="search-submit"]').click()


    # Select product
    page.locator("a").filter(has_text="Combination Pliers").first.click()
    print("Product selected")
    page.wait_for_load_state("networkidle")


    # Add product to cart
    page.get_by_role("button",name="Add to cart").click()
    print("Product added to cart")


    # Open cart
    page.locator('[data-test="nav-cart"]').click()
    print("Cart opened")


    # Proceed to checkout
    page.get_by_role("button",name="Proceed to checkout").click()
    print("Checkout page opened")



    #Select Continue as Guest tab
    guest_tab = page.get_by_role("tab",name="Continue as Guest")
    expect(guest_tab).to_be_visible()
    guest_tab.click()
    print("Continue as Guest tab selected")


    #Enter guest information
    guest_email = page.locator('[data-test="guest-email"]')
    guest_first_name = page.locator('[data-test="guest-first-name"]')
    guest_last_name = page.locator('[data-test="guest-last-name"]')
    expect(guest_email).to_be_visible()
    expect(guest_first_name).to_be_visible()
    expect(guest_last_name).to_be_visible()
    guest_email.fill("deepakvb01@gmail.com")
    guest_first_name.fill("Arun")
    guest_last_name.fill("Deepak")
    print("Valid guest information entered")


    # Continue as Guest
    page.locator('[data-test="guest-submit"]').click()
    print("Continue as Guest clicked")
    page.wait_for_load_state("networkidle")
    print("Moved to next checkout step")


    # Verify we moved forward
    print("Current URL:", page.url)
 


    # SCENARIO 2 - MISSING MANDATORY INFORMATION
    print("Scenario 2 - Missing Mandatory Information")
    page.goto("https://practicesoftwaretesting.com/")


    # Search product
    page.locator('[data-test="search-query"]').fill("Combination Pliers")
    page.locator('[data-test="search-submit"]').click()



    # Select product
    page.locator("a").filter(has_text="Combination Pliers").first.click()
    print("Product selected")
    page.wait_for_load_state("networkidle")



    # Add product
    page.get_by_role("button",name="Add to cart").click()
    print("Product added to cart")


    # Open cart
    page.locator('[data-test="nav-cart"]').click()
    print("Cart opened")

    # Proceed to checkout
    page.get_by_role("button",name="Proceed to checkout").click()
    print("Checkout page opened")


    # Select Guest tab
    page.get_by_role("tab",name="Continue as Guest").click()
    print("Continue as Guest tab selected")

    # Leave all fields empty
    page.locator('[data-test="guest-submit"]').click()
    print("Submitted empty form")

    # Verify checkout did not proceed
    expect(page.locator('[data-test="guest-email"]')).to_be_visible()

    expect(page.locator('[data-test="guest-first-name"]')).to_be_visible()

    expect(page.locator('[data-test="guest-last-name"]')).to_be_visible()

    print("Mandatory field validation displayed")
    print("Checkout was blocked")




    # SCENARIO 3 - INVALID INFORMATION
    print("Scenario 3 - Invalid Information")
    page.goto("https://practicesoftwaretesting.com/")


    # Search product
    page.locator('[data-test="search-query"]').fill("Combination Pliers")
    page.locator('[data-test="search-submit"]').click()



    # Select product
    page.locator("a").filter(has_text="Combination Pliers").first.click()
    print("Product selected")
    page.wait_for_load_state("networkidle")


    # Add product
    page.get_by_role("button",name="Add to cart").click()
    print("Product added to cart")


    # Open cart
    page.locator('[data-test="nav-cart"]').click()
    print("Cart opened")


    # Proceed to checkout
    page.get_by_role("button",name="Proceed to checkout").click()
    print("Checkout page opened")


    # Select Guest tab
    page.get_by_role("tab",name="Continue as Guest").click()
    print("Continue as Guest tab selected")


    # Invalid email
    page.locator('[data-test="guest-email"]').fill("invalid-email")

    # Valid names
    page.locator('[data-test="guest-first-name"]').fill("Arun")
    page.locator('[data-test="guest-last-name"]').fill("Deepak")
    print("Invalid email entered")

    # Submit
    page.locator('[data-test="guest-submit"]').click()
    print("Submitted invalid information")

    # Verify checkout did not proceed
    expect(page.locator('[data-test="guest-email"]')).to_be_visible()

    print("Invalid information rejected")
    print("Checkout was blocked")



    # SCENARIO 4 - CART CONSISTENCY
    print("Scenario 4 - Cart Consistency")
    page.goto("https://practicesoftwaretesting.com/")


    # Search product
    page.locator('[data-test="search-query"]').fill("Combination Pliers")
    page.locator('[data-test="search-submit"]').click()


    # Select product
    page.locator("a").filter(has_text="Combination Pliers").first.click()
    print("Product selected")
    page.wait_for_load_state("networkidle")


    # Add product
    page.get_by_role("button",name="Add to cart").click()
    print("Product added to cart")


    # Open cart
    page.locator('[data-test="nav-cart"]').click()
    print("Cart opened")


    # Capture cart information
    product_name = page.locator('[data-test="product-title"]').first.inner_text()
    product_price = page.locator('[data-test="product-price"]').first.inner_text()
    quantity = page.locator('[data-test="product-quantity"]').first.input_value()
    total = page.locator('[data-test="cart-total"]').inner_text()
    print("\nBefore Checkout")
    print("Product Name:", product_name)
    print("Product Price:", product_price)
    print("Quantity:", quantity)
    print("Total:", total)


    # Proceed to checkout
    page.get_by_role("button",name="Proceed to checkout").click()
    print("\nCheckout page opened")


    # Cart information should still be available
    checkout_product_name = page.locator('[data-test="product-title"]').first.inner_text()
    checkout_product_price = page.locator('[data-test="product-price"]').first.inner_text()
    checkout_quantity = page.locator('[data-test="product-quantity"]').first.input_value()
    checkout_total = page.locator('[data-test="cart-total"]').inner_text()

    print("\nAfter Checkout")
    print("Product Name:", checkout_product_name)
    print("Product Price:", checkout_product_price)
    print("Quantity:", checkout_quantity)
    print("Total:", checkout_total)

    # Verify consistency
    assert checkout_product_name == product_name
    print("Product name matches")

    assert checkout_product_price == product_price
    print("Product price matches")

    assert checkout_quantity == quantity
    print("Quantity matches")

    assert checkout_total == total
    print("Total matches")


    browser.close()