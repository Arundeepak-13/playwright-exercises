from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Open application
    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_timeout(2000)
    print("Product listing page opened")



    products = page.locator('[data-test^="product-"]')
    page.wait_for_timeout(2000)
    product_count = products.count()
    print(f"Total products found: {product_count}")


    for i in range(product_count):
        product = products.nth(i)
        product_name = product.locator(
            '[data-test="product-name"]'
        ).text_content().strip()
        product_text = product.inner_text().lower()
        if "out of stock" in product_text:
            print(f"Skipping unavailable product: {product_name}")
            continue
        print(f"First available product: {product_name}")


    

        # Click product
        product.click()
        page.wait_for_timeout(2000)



        # Wait for product details page
        page.wait_for_url("**/product/**")
        page.wait_for_timeout(2000)
        assert "/product/" in page.url
        print("Product details page opened successfully")
        break

    browser.close()