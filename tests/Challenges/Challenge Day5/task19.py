from playwright.sync_api import sync_playwright, expect


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()


    # Open product listing
    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_load_state("networkidle")

    # Wait for products
    page.locator('[data-test="product-name"]').first.wait_for(state="visible")

    # Get product names and prices
    products = page.locator('[data-test="product-name"]')
    prices = page.locator('[data-test="product-price"]')

    print("Total products:", products.count())

    # Test first 5 products
    for i in range(5):
        print("\nTesting Product", i + 1)


        # Get name from listing page
        listing_name = products.nth(i).inner_text().strip()


        # Get price from listing page
        listing_price = prices.nth(i).inner_text().strip()


        print("Listing Name :", listing_name)
        print("Listing Price:", listing_price)


        # Open product
        products.nth(i).click()
        page.wait_for_load_state("networkidle")


        # Get name from details page
        details_name = page.locator('[data-test="product-name"]').inner_text().strip()


        # Get price from details page
        details_price = page.get_by_text(listing_price).inner_text().strip()


        print("Details Name :", details_name)
        print("Details Price:", details_price)


        # Verify product name
        expect(page.locator('[data-test="product-name"]')).to_have_text(listing_name)


        # Verify product price
        expect(page.get_by_text(listing_price)).to_have_text(listing_price)
        print("Product", i + 1, "PASSED")


        # Go back to listing page
        page.go_back()
        page.wait_for_load_state("networkidle")


        # Wait for products again
        page.locator('[data-test="product-name"]').first.wait_for(
            state="visible"
        )


    browser.close()