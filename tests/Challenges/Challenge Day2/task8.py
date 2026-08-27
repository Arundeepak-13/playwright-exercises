from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://practicesoftwaretesting.com/")
    print("Application opened")

    # Select a product
    product = page.get_by_text("Claw Hammer with Shock Reduction Grip")
    product.click()
    print("Product opened")
    page.wait_for_timeout(2000)


    # Get product price
    price_text = page.locator('[data-test="unit-price"]').inner_text()
    price = float(price_text.replace("$", "").strip())
    print(f"Product price: ${price}")
    page.wait_for_timeout(1000)


    # Change quantity to 3
    quantity = page.locator('[data-test="quantity"]')
    quantity.fill("3")
    print("Quantity changed to 3")

    page.wait_for_timeout(1000)

    # Add product to cart
    page.get_by_role("button", name="Add to cart").click()
    print("Product added to cart")

    # Open cart
    page.get_by_text("Cart").click()
    print("Cart opened")

    # Verify quantity
    cart_quantity = page.locator('[data-test="quantity"]').input_value()
    assert cart_quantity == "3"
    print("Quantity verified: 3")


    # Calculate expected total
    expected_total = round(price * 3, 2)
    total_text = page.locator('[data-test="cart-total"]').inner_text()
    actual_total = float(total_text.replace("$", "").strip())
    print(f"Expected total: ${expected_total}")
    print(f"Actual total: ${actual_total}")
    assert actual_total == expected_total
    print("Total price verified successfully")

        

    page.wait_for_timeout(3000)

    browser.close()