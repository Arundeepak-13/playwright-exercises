from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Open application
    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_timeout(1000)

    # Wait for products
    page.locator("a[href^='/product/']").first.wait_for()

    print("Application opened")

    # Get all products
    products = page.locator("a[href^='/product/']")
    product_count = products.count()

    print("Number of products:", product_count)

    # Verify products are displayed
    assert product_count > 0, "No products are displayed"
    print("Products are displayed")

    # Initialize cheapest product
    cheapest_price = float("inf")
    cheapest_product = ""

    # Loop through all products
    for i in range(product_count):

        product = products.nth(i)

        # Get product name
        product_name = product.locator(
            '[data-test="product-name"]'
        ).inner_text().strip()

        # Validate product name
        assert product_name != "", \
            f"Product name is empty for product {i + 1}"

        # Get product price
        price_text = product.locator('[data-test="product-price"]').inner_text().strip()

        # Validate price is not empty
        assert price_text != "", \
            f"Product price is empty for {product_name}"

        # Convert price text to number
        price = float(price_text.replace("$", ""))

        # Print product and price
        print(f"{product_name} - {price_text}")

        # Find cheapest product
        if price < cheapest_price:
            cheapest_price = price
            cheapest_product = product_name

    # Print cheapest product
    print()
    print("Cheapest Product:")
    print(f"{cheapest_product} - ${cheapest_price:.2f}")

    # Keep browser open for 3 seconds
    page.wait_for_timeout(3000)

    # Close browser
    browser.close()