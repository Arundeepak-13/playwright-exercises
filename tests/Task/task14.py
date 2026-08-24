from playwright.sync_api import sync_playwright, expect


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    products = [
        "Combination Pliers",
        "Bolt Cutters",
        "Claw Hammer"
    ]

    for search_product in products:

        print("Testing:", search_product)
        # Open application
        page.goto("https://practicesoftwaretesting.com/")
        print("Application opened successfully")



        # Search product
        search = page.locator('[data-test="search-query"]')
        expect(search).to_be_visible()
        search.fill(search_product)
        search.press("Enter")
        print("Product searched")



        # Select product from search results
        product = page.locator('[data-test="product-name"]').first
        expect(product).to_be_visible()
        product.click()
        print("Product selected")



        # Capture product name
        product_name_locator = page.locator('[data-test="product-name"]').first
        expect(product_name_locator).to_be_visible()
        actual_product_name = product_name_locator.inner_text().strip()
        print("Product name:", actual_product_name)



        # Verify searched product is part of actual product name
        assert search_product.lower() in actual_product_name.lower()


        # Capture product price
        price = page.locator('[data-test="unit-price"]').first
        expect(price).to_be_visible()
        price_text = price.inner_text().strip()
        product_price = float(price_text.replace("$", "").replace(",", ""))
        print("Product price:", product_price)
        assert product_price > 0


        # Add product to cart
        add_to_cart = page.locator('[data-test="add-to-cart"]')
        expect(add_to_cart).to_be_visible()
        expect(add_to_cart).to_be_enabled()
        add_to_cart.click()
        print("Product added to cart")



        # Open cart
        cart = page.locator('[data-test="nav-cart"]')
        expect(cart).to_be_visible()
        cart.click()
        print("Cart opened")



        # Verify correct product is present
        cart_product = page.locator('[data-test="product-title"]').first
        expect(cart_product).to_be_visible()
        assert actual_product_name in cart_product.inner_text()
        print("Correct product is present")



        # Verify cart price
        cart_price = page.locator('[data-test="product-price"]').first
        expect(cart_price).to_be_visible()
        cart_price_text = cart_price.inner_text().strip()
        cart_product_price = float(cart_price_text.replace("$", "").replace(",", ""))
        print("Product page price:", product_price)
        print("Cart price:", cart_product_price)
        assert cart_product_price == product_price
        print("Price matches")



        # Change quantity to 2
        quantity = page.locator('[data-test="product-quantity"]').first
        expect(quantity).to_be_visible()
        quantity.fill("2")
        expect(quantity).to_have_value("2")
        print("Quantity changed to 2")


        # Calculate expected total
        expected_total = product_price * 2
        print("Expected total:", expected_total)


        # Calculate actual total
        prices = page.locator('[data-test="product-price"]')
        quantities = page.locator('[data-test="product-quantity"]')
        actual_total = 0
        for i in range(prices.count()):
            price_text = prices.nth(i).inner_text().strip()
            price_value = float(price_text.replace("$", "").replace(",", ""))
            quantity_value = int(quantities.nth(i).input_value())
            actual_total = actual_total + (price_value * quantity_value)
        print("Actual total:", actual_total)
        assert actual_total == expected_total
        print("Cart total is correct")


        # Find product row
        product_row = page.locator("tr",has_text=actual_product_name).first
        expect(product_row).to_be_visible()


        # Last cell contains the remove control
        remove_cell = product_row.locator("td").last
        expect(remove_cell).to_be_visible()


        # Find any clickable element in the last cell
        remove_element = remove_cell.locator("a, button, input, [role='button']").first


        # Check that remove element exists
        assert remove_element.count() > 0
        expect(remove_element).to_be_visible()


        # Click remove
        remove_element.click()
        print("Product removed")


        # Verify product is removed
        expect(page.locator("tr",has_text=actual_product_name)).to_have_count(0)
        print("Product is no longer in cart")



        # Verify cart is empty
        cart_items = page.locator("table tbody tr")
        expect(cart_items).to_have_count(0)
        print("Cart is empty")

    browser.close()
