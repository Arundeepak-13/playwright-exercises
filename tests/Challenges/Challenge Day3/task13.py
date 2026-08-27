from playwright.sync_api import expect, sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_timeout(1000)

  
    page.locator('img[alt="Slip Joint Pliers"]').click()
    page.wait_for_timeout(1000)

    price_a = float(page.locator('span[aria-label="unit-price"]').text_content().strip())
    print("Product A price:", price_a)

    add_to_cart_a = page.get_by_role('button', name='Add to Cart')
    add_to_cart_a.click()
    print(add_to_cart_a.text_content())
    page.wait_for_timeout(1000)

    page.go_back()
    page.wait_for_timeout(1000)

    
    page.locator('img[alt="Bolt Cutters"]').click()
    page.wait_for_timeout(1000)

    price_b = float(page.locator('span[aria-label="unit-price"]').text_content().strip())
    print("Product B price:", price_b)

    add_to_cart_b = page.get_by_role('button', name='Add to Cart')
    add_to_cart_b.click()
    print(add_to_cart_b.text_content())
    page.wait_for_timeout(1000)

   
    page.locator('[data-test="nav-cart"]').click()
    page.wait_for_timeout(1000)
    expect(page.locator('[data-test="product-title"]'))

    quantities = page.locator('[data-test="product-quantity"]')

    quantity_a = float(quantities.nth(0).input_value())
    quantity_b = float(quantities.nth(1).input_value())
    print("Quantity A:", quantity_a, "Quantity B:", quantity_b)

   
    expected_total = round((price_a * quantity_a) + (price_b * quantity_b), 2)
    print("Expected total:", expected_total)

    
    browser.close()